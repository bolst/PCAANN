namespace PCAANN.Data;

public class PRange
{
    public int Start { get; set; }
    public int Stop { get; set; }
    public int Step { get; set; }

    public bool Enabled { get; set; }

    public PRange(int start = 0, int stop = 0, int step = 1)
    {
        Start = start;
        Stop = stop;
        Step = step;
        Enabled = (Start < Stop) && (Step > 0);
    }
}