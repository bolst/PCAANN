using PCAANN.Data;

public class OptionProfileController
{
    #region singleton
    private static OptionProfileController? instance = null;
    private OptionProfileController() { }
    public static OptionProfileController Instance()
    {
        if (instance == null) instance = new OptionProfileController();
        instance.GetOptions();
        return instance;
    }
    #endregion

    private void GetOptions()
    {
        OptionProfile inst = OptionProfile.Instance();

        components = (int)inst.NumComponents.Value();
        fullSpectrum = (bool)inst.FullSpectrum.Value();
        framework = inst.Framework.Value().ToString();
        optimizer = inst.Optimizer.Value().ToString();
        activation = inst.Activation.Value().ToString();
        loss = inst.Loss.Value().ToString();
        Console.WriteLine(inst.Epochs.Value() + "\n\n\n");
        epochs = inst.Epochs.Value().ToString();
        batchSize = inst.BatchSize.Value().ToString();
        patience = inst.Patience.Value().ToString();
        hiddenNodes = inst.HiddenNodes.Value().ToString();
        runs = (int)inst.Runs.Value();
        classNumber = (int)inst.ClassNumber.Value();
    }

    public string? rawDataFilename { get; set; }
    public string? pcaScoresFilename { get; set; }
    public int? components { get; set; }
    public bool? fullSpectrum { get; set; }
    public string? framework { get; set; }
    public string? optimizer { get; set; }
    public string? activation { get; set; }
    public string? loss { get; set; }
    public string? epochs { get; set; }
    public string? batchSize { get; set; }
    public string? patience { get; set; }
    public string? hiddenNodes { get; set; }
    public int? runs { get; set; }
    public int? classNumber { get; set; }
}