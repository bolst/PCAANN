namespace PCAANN.Api;

public class StateService
{

    private static StateService? instance = null;


    private StateService() { }

    public static StateService Instance()
    {
        if (instance == null) instance = new StateService();
        return instance;
    }

    public STATE State { get; set; }

    public enum STATE
    {
        Init = 0,
        RawDataLoaded = 1,
        PcaRan = 2,
        PcaScoresLoaded = 3,
        AnnRan = 4
    }
}