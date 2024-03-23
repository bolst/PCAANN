namespace PCAANN.Data;

public class RangeableOptionProfileItem : IOptionProfileItem
{
    private string label { get; }

    public int value;

    public PRange Range;

    public RangeableOptionProfileItem(string l, int v, int start = 0, int stop = 0, int step = 0)
    {
        label = l;
        value = v;
        Range = new PRange(start, stop, step);
    }

    public string Label() { return label; }

    public object Value() { return Range.Enabled ? $"{value} {Range.Start} {Range.Stop} {Range.Step}" : value; }

    public string Type() { return "range"; }

    public bool Enabled() { return Range.Enabled; }
}