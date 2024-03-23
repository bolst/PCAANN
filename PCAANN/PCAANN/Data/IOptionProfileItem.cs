namespace PCAANN.Data;

public interface IOptionProfileItem
{

    bool IsType<T>()
    {
        return this.GetType() == typeof(T);
    }

    string Label();

    string Id() { return String.Concat(Label().Where(c => !Char.IsWhiteSpace(c))); }

    object Value();

    string Type();

    bool Enabled();

    string ToJson()
    {
        string id = Label();
        string type = Type();
        object value = Value();
        try
        {
            value = (int)value;
        }
        catch
        {
            value = $@"""{value}""";
        }
        string enabled = Enabled() ? "true" : "false";

        return $@"
        {{
            ""id"": ""{id}"",
            ""type"": ""{type}"",
            ""value"": {value},
            ""enabled"": {enabled}
        }}
        ";
    }

}