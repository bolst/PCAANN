namespace PCAANN.Api;

public class BkLoadPcaScores : AbstractBk
{
    protected override async Task<string> Call()
    {
        var response = await client.PostAsJsonAsync<OptionProfileController>($"{UriBase()}/loadpca", OptionProfileController.Instance());

        if (response.IsSuccessStatusCode)
        {
            string response_value = await response.Content.ReadAsStringAsync();
            return response_value;
        }

        Console.WriteLine("Hello from load pca scores!");
        return "success";
    }

    public override StateService.STATE StateAfterCompletion() { return StateService.STATE.PcaScoresLoaded; }

    public override bool IsComplete() { return StateService.Instance().State >= StateService.STATE.PcaScoresLoaded; }

    public override bool IsCallable() { return true; }

}