using System.Reflection.Emit;
using Blazorise.Extensions;

namespace PCAANN.Api;

public class BkLoadRaw : AbstractBk
{
    protected override async Task<string> Call()
    {
        var response = await client.PostAsJsonAsync<OptionProfileController>($"{UriBase()}/loadfile", OptionProfileController.Instance());

        string response_value = await response.Content.ReadAsStringAsync();
        Console.WriteLine("Hello from load raw data!");
        if (response_value != "success")
        {
            return "error, see <<todo>> for more details";
        }
        return response_value;
    }

    public override StateService.STATE StateAfterCompletion() { return StateService.STATE.RawDataLoaded; }

    public override bool IsComplete() { return StateService.Instance().State >= StateService.STATE.RawDataLoaded; }

    public override bool IsCallable() { return StateService.Instance().State >= StateService.STATE.Init; }
}
