
namespace PCAANN.Pages
{
    public partial class Index
    {
        private bool ConnectionEstablished = false;
        private const int MAX_CONNECTION_ATTEMPTS = 10;


        protected override async Task OnAfterRenderAsync(bool firstRender)
        {
            if (ConnectionEstablished == false)
                await WaitForConnection();
        }

        private async Task WaitForConnection()
        {
            int ConnectionAttempts = 0;
            while (ConnectionAttempts++ < MAX_CONNECTION_ATTEMPTS)
            {
                Console.WriteLine($"connection attempt {ConnectionAttempts}");
                var status = await Api.DataExchange.TestConnection();
                if (status == true)
                {
                    ConnectionEstablished = true;
                    StateHasChanged();
                    break;
                }
                Thread.Sleep(2000);
            }
        }

        private string ToolContent = @"<p>The app can't establish a connection with the PCA/ANN code server. Try the following:</p>
                                        <ol>
                                            <li>Make sure the server is running.</li>
                                            <li>The server may take a few seconds to start. Reload the page.</li>
                                            <li>If the app still can't find the server, there may be a problem with how the connection is being established. Refer to the SOP.</li>
                                        </ol>";

    }
}