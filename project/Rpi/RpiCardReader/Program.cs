// Imports
using System.Device.Gpio;
using System.Device.Spi;
using Iot.Device.DHTxx;
using Iot.Device.Mfrc522;
using Iot.Device.Rfid;
using UnitsNet;
using Newtonsoft.Json;
using System.Threading;

// Consts
const int APP_WAIT_TIME = 5000;

// HttpClient declaration
HttpClient client = new HttpClient();


// Convert RFID card to HEX
string GetCardId(Data106kbpsTypeA card) => Convert.ToHexString(card.NfcId);

// GpioController declaration
GpioController gpioController = new GpioController();

// Pins preparation
int pinReset = 21;
int pinGreen = 22;
int pinYellow = 23;
int pinRed = 24;
int pinDht = 16; 

// Pins opening
gpioController.OpenPin(pinGreen, PinMode.Output);
gpioController.OpenPin(pinYellow, PinMode.Output);
gpioController.OpenPin(pinRed, PinMode.Output);

// Dht11 sensor declaration
Dht11 dhtSensor = new Dht11(pinDht);

SpiConnectionSettings connection = new(0, 0);
connection.ClockFrequency = 10_000_000;

string fileName = "config.json";
string configString = File.ReadAllText(fileName);
dynamic config = JsonConvert.DeserializeObject(configString)!;
string url = "";

foreach (var item in config)
{
    if (item.Name == "url")
    {
        url = item.Value;
    }
}

var source = new CancellationTokenSource();
var token = source.Token;

var task = Task.Run(() => ReadData(token), token);

Console.WriteLine("Press any key to close.");
Console.ReadKey();

source.Cancel();

await task;

void welcomeBlink(){
    var onTime = 500;
    var offTime = 300;
    var iterations = 3;
    for(int i = 0; i < iterations; i++){
        gpioController.Write(pinGreen, PinValue.High);
        gpioController.Write(pinYellow, PinValue.High);
        gpioController.Write(pinRed, PinValue.High);
        Thread.Sleep(onTime);
        gpioController.Write(pinGreen, PinValue.Low);
        gpioController.Write(pinYellow, PinValue.Low);
        gpioController.Write(pinRed, PinValue.Low);
        Thread.Sleep(offTime);
    }
    
}

void ledBlinking(int ledPin, int sleepTime, int iterations){
    for(int i = 0; i < iterations; i++){
        gpioController.Write(ledPin, PinValue.High);
        Thread.Sleep(sleepTime);
        gpioController.Write(ledPin, PinValue.Low);
        Thread.Sleep(sleepTime);
    }
}

double ReadTemperature(Dht11 dhtSensorName){


    if (!dhtSensorName.TryReadHumidity(out RelativeHumidity humidity))
    {
        Console.WriteLine("Can't read humidity");
        return 0;
    }
    
    return humidity.Value;
}

void ReadData(CancellationToken cancellationToken)
{
    Console.WriteLine("Starting reading from RFID reader");
    welcomeBlink();

    var active = true;

    do
    {
        if (cancellationToken.IsCancellationRequested)
        {
            active = false;
        }

        try
        {
            using (SpiDevice spi = SpiDevice.Create(connection))
            using (MfRc522 mfrc522 = new(spi, pinReset, gpioController, false))
            {

                Data106kbpsTypeA card;
                var res = mfrc522.ListenToCardIso14443TypeA(out card, TimeSpan.FromSeconds(2));

                if (res)
                {
                    var cardId = GetCardId(card);
                    Console.WriteLine("Card read: " + cardId);

                    var data = new Dictionary<string, string>();
                    var now = DateTime.Now;
                    var format = "yyyy-MM-dd HH:mm:ss";
                    data.Add("log_time", now.ToString(format));
                    data.Add("card_id", cardId);
                    Console.WriteLine(ReadTemperature(dhtSensor));
                    SendHttpRequest(url, data);
                    gpioController.Write(pinYellow, PinValue.High);
                    Thread.Sleep(APP_WAIT_TIME);
                    gpioController.Write(pinYellow, PinValue.Low);
                }
            }

        }
        catch (System.Exception ex)
        {
            Console.WriteLine(ex.Message);
            throw;
        }
    } while (active);

    Console.WriteLine("Reading finished.");
}

void SendHttpRequest(String url, Dictionary<string, string> data)
{
    Console.WriteLine("Sending HTTP request");
    var method = new HttpMethod("POST");
    var request = new HttpRequestMessage(method, url);
    var jsonData = JsonConvert.SerializeObject(data);
    request.Content = new StringContent(jsonData, System.Text.Encoding.UTF8, "application/json");
    var response = client.Send(request);
    var responseStatus = response.IsSuccessStatusCode;

    if(responseStatus){
        ledBlinking(pinGreen, 500, 2);
    }
    else{
        ledBlinking(pinRed, 500, 2);
    }

    Console.WriteLine("HTTP request sent, response received");
}