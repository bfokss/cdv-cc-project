using System.Device.Gpio;
using System.Device.Spi;
using Iot.Device.Mfrc522;
using Iot.Device.Rfid;
using Newtonsoft.Json;

HttpClient client = new HttpClient();

string GetCardId(Data106kbpsTypeA card) => Convert.ToHexString(card.NfcId);

GpioController gpioController = new GpioController();
int pinReset = 21;

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

void ReadData(CancellationToken cancellationToken)
{
    Console.WriteLine("Starting reading from RFID reader");
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
                    var format = "yyyy-MM-dd hh:mm:ss";
                    data.Add("log_time", now.ToString(format));
                    data.Add("card_id", cardId);
                    SendHttpRequest(url, data);
                    Thread.Sleep(3000);
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

    Console.WriteLine("HTTP request sent");
}