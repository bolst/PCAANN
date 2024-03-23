namespace PCAANN.Api;

public static class DataExchange
{

    public static async Task<List<string>?> GetRawDataFiles()
    {
        HttpClient client = new HttpClient();
        var response = await client.GetAsync($"{UriBase.Uri()}/raw-data/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }
    public static async Task<List<string>?> GetScoresFiles()
    {
        HttpClient client = new HttpClient();
        var response = await client.GetAsync($"{UriBase.Uri()}/scores/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }
    public static async Task<List<string>?> GetResultsFiles()
    {
        HttpClient client = new HttpClient();
        var response = await client.GetAsync($"{UriBase.Uri()}/results/files");
        List<string>? retval = await response.Content.ReadFromJsonAsync<List<string>>();
        return retval;
    }

}
