using System.Text.Json;

namespace PCAANN.Data;

public class OptionProfile
{

    #region Options for (some) Parameters

    private readonly List<string> FRAMEWORK_OPTIONS = new List<string>() { "TensorFlow", "Scikit-Learn" };
    private readonly List<string> OPTIMIZER_OPTIONS = new List<string>() { "adam" };
    private readonly List<string> ACTIVATION_OPTIONS = new List<string>() { "relu" };
    private readonly List<string> LOSS_OPTIONS = new List<string>() { "binary_crossentropy", "categorical_crossentropy" };

    #endregion

    #region PCA Parameters

    public IOptionProfileItem NumComponents { get; set; }

    public IOptionProfileItem FullSpectrum { get; set; }

    #endregion

    #region ANN Parameters

    public IOptionProfileItem Framework { get; set; }
    public IOptionProfileItem Optimizer { get; set; }
    public IOptionProfileItem Activation { get; set; }
    public IOptionProfileItem Loss { get; set; }
    public IOptionProfileItem Epochs { get; set; }
    public IOptionProfileItem BatchSize { get; set; }
    public IOptionProfileItem Patience { get; set; }
    public IOptionProfileItem HiddenNodes { get; set; }
    public IOptionProfileItem Runs { get; set; }
    public IOptionProfileItem ClassNumber { get; set; }

    #endregion

    #region singleton
    private static OptionProfile? instance = null;

    private OptionProfile()
    {
        NumComponents = new NumericalInputOptionProfileItem("Number of Components", 3);
        FullSpectrum = new BoolOptionProfileItem("Full Spectrum");

        Framework = new SelectOptionProfileItem("Framework", FRAMEWORK_OPTIONS, FRAMEWORK_OPTIONS[0]);
        Optimizer = new SelectOptionProfileItem("Optimizer", OPTIMIZER_OPTIONS, OPTIMIZER_OPTIONS[0]);
        Activation = new SelectOptionProfileItem("Activation", ACTIVATION_OPTIONS, ACTIVATION_OPTIONS[0]);
        Loss = new SelectOptionProfileItem("Loss", LOSS_OPTIONS, LOSS_OPTIONS[0]);
        Epochs = new RangeableOptionProfileItem("Epochs", 200, 200, 350, 100);
        BatchSize = new RangeableOptionProfileItem("Batch Size", 64, 20, 50, 5);
        Patience = new RangeableOptionProfileItem("Patience", 10, 5, 50, 5);
        HiddenNodes = new RangeableOptionProfileItem("Hidden Nodes", 100, 80, 180, 10);
        Runs = new NumericalInputOptionProfileItem("Runs", 3);
        ClassNumber = new NumericalInputOptionProfileItem("Class Number", 4);

    }

    public static OptionProfile Instance()
    {
        if (instance == null) instance = new OptionProfile();
        return instance;
    }

    #endregion

    // Note to readers: im sorry
    public void Update(string pathToJson)
    {
        try
        {
            string rawJsonStr = File.ReadAllText(pathToJson);
            var dataList = JsonSerializer.Deserialize<List<DataRoot>>(rawJsonStr);

            NumComponents = new NumericalInputOptionProfileItem(dataList[0].id, int.Parse(dataList[0].value.ToString()));
            FullSpectrum = new BoolOptionProfileItem(dataList[1].id, bool.Parse(dataList[1].value.ToString()));

            Framework = new SelectOptionProfileItem(dataList[2].id, FRAMEWORK_OPTIONS, dataList[2].value.ToString());
            Optimizer = new SelectOptionProfileItem(dataList[3].id, OPTIMIZER_OPTIONS, dataList[3].value.ToString());
            Activation = new SelectOptionProfileItem(dataList[4].id, ACTIVATION_OPTIONS, dataList[4].value.ToString());
            Loss = new SelectOptionProfileItem(dataList[5].id, LOSS_OPTIONS, dataList[5].value.ToString());
            Epochs = ParseRangeable(dataList[6]);
            BatchSize = ParseRangeable(dataList[7]);
            Patience = ParseRangeable(dataList[8]);
            HiddenNodes = ParseRangeable(dataList[9]);
            Runs = new NumericalInputOptionProfileItem(dataList[10].id, int.Parse(dataList[10].value.ToString()));
            ClassNumber = new NumericalInputOptionProfileItem(dataList[11].id, int.Parse(dataList[11].value.ToString()));
        }
        catch (Exception exc) { Console.WriteLine(exc.ToString()); }
    }


    private RangeableOptionProfileItem ParseRangeable(DataRoot r)
    {
        if (r.enabled)
        {
            string[] rangeArray = r.value.ToString().Split(' ');
            int val = int.Parse(rangeArray[0]);
            int start = int.Parse(rangeArray[1]);
            int stop = int.Parse(rangeArray[2]);
            int step = int.Parse(rangeArray[3]);
            return new RangeableOptionProfileItem(r.id, val, start, stop, step);
        }
        return new RangeableOptionProfileItem(r.id, int.Parse(r.value.ToString()));
    }

    public string ToJson()
    {
        return $@"[{NumComponents.ToJson()},{FullSpectrum.ToJson()},{Framework.ToJson()},{Optimizer.ToJson()},{Activation.ToJson()},{Loss.ToJson()},{Epochs.ToJson()},{BatchSize.ToJson()},{Patience.ToJson()},{HiddenNodes.ToJson()},{Runs.ToJson()},{ClassNumber.ToJson()}]";
    }

    // Root myDeserializedClass = JsonConvert.DeserializeObject<List<Root>>(myJsonResponse);
    private class DataRoot
    {
        public string id { get; set; }
        public string type { get; set; }
        public object value { get; set; }
        public bool enabled { get; set; }
    }


}