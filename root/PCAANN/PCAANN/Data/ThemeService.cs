namespace PCAANN.Data;

public class ThemeService
{

    private static ThemeService? instance;

    public readonly string Primary;
    public readonly string Secondary;
    public readonly string Success;
    public readonly string Warning;
    public readonly string Dark;
    public readonly string White;
    public readonly string Black;

    public static ThemeService Instance()
    {
        if (instance == null) instance = new ThemeService();
        return instance;
    }

    private ThemeService()
    {
        Primary = "#5c8cff"; // blue
        Secondary = "#BC62B7"; // purple
        Success = "#31AF51"; // green
        Warning = "#DF2935"; // red
        Dark = "#212738"; // navy blue
        White = "#E6E8E6";
        Black = "#080708";
    }
}