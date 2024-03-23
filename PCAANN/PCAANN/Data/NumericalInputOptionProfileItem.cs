namespace PCAANN.Data;

public class NumericalInputOptionProfileItem : IOptionProfileItem
{

    public int value { get; set; }

    private string label { get; }

    public NumericalInputOptionProfileItem(string label, int val)
    {
        value = val;
        this.label = label;
    }

    public string Label() { return label; }

    public object Value() { return value; }

    public string Type() { return "numerical"; }

    public bool Enabled() { return true; }

}