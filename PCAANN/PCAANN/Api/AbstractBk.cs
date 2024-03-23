namespace PCAANN.Api;

public abstract class AbstractBk
{

    protected string ErrorMessage { get; set; } = "";

    protected HttpClient client = new HttpClient();

    protected abstract Task<string> Call();

    public abstract bool IsCallable();

    public abstract bool IsComplete();

    public abstract StateService.STATE StateAfterCompletion();

    public async Task<bool> Perform()
    {
        // to ensure the http request doesn't time out while waiting for pca/ann to run
        client.Timeout = TimeSpan.FromMinutes(10);

        if (IsCallable())
        {
            Task<string> statusCall = Call();

            try
            {
                string retval = await statusCall;
                if (retval == "success")
                {
                    StateService.Instance().State = StateAfterCompletion();
                    return true;
                }
                else
                {
                    ErrorMessage = retval;
                    return false;
                }
            }
            catch (HttpRequestException)
            {
                ErrorMessage = "Connection error with PCA/ANN";
                return false;
            }
            catch (Exception e)
            {
                ErrorMessage = e.ToString();
                return false;
            }
        }
        else
        {
            Console.WriteLine("Not there yet");
        }

        return false;
    }

    protected string UriBase() { return Api.UriBase.Uri(); }

    public string GetError() { return ErrorMessage; }


}