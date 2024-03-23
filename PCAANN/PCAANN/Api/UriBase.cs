namespace PCAANN.Api
{
    public static class UriBase
    {
        private const bool Dev = false;
        public static string Uri()
        {
            return Dev ? @"http://127.0.0.1:8000/" : @"http://host.docker.internal:8000/";
        }
    }
}
