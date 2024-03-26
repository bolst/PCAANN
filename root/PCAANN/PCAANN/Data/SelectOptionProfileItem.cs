namespace PCAANN.Data;

public class SelectOptionProfileItem : IOptionProfileItem
{

    private string label { get; }

    public List<string> Options { get; }

    public string value { get; set; }

    public SelectOptionProfileItem(string l, List<string> options, string val)
    {
        label = l;
        Options = options;
        value = val;
    }

    public string Label()
    {
        return label;
    }

    public object Value() { return value; }

    public string Type() { return "selectable"; }

    public bool Enabled() { return true; }

}