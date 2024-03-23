namespace PCAANN.Data;

public class BoolOptionProfileItem : IOptionProfileItem
{

    private string label;

    public bool value;

    public BoolOptionProfileItem(string l, bool v = true)
    {
        label = l;
        value = v;
    }

    public string Label() { return label; }

    public object Value() { return value; }

    public string Type() { return "bool"; }

    public bool Enabled() { return true; }

}

