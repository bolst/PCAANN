namespace PCAANN.Api;

public class BkViewResults : AbstractBk
{
    protected override async Task<string> Call()
    {

        var response = await client.GetAsync($"{UriBase()}/viewresults");
        if (response.IsSuccessStatusCode)
        {
            string response_value = await response.Content.ReadAsStringAsync();
            return response_value;
        }

        Console.WriteLine("Hello from view results!");
        return "success";
    }

    public override StateService.STATE StateAfterCompletion() { return StateService.Instance().State; }

    public override bool IsComplete() { return StateService.Instance().State >= StateService.STATE.AnnRan; }

    public override bool IsCallable() { return StateService.Instance().State >= StateService.STATE.AnnRan; }


}