function DecodeCovidPayload(data){
    var obj = {};
    var curIndex = 0;

    function hexToInt(length){
        var vals = data.slice(curIndex, curIndex + length);
        var strValue = '0x';
        for (i in vals) {
            strValue += ('00' + vals[i].toString(16)).slice(-2);
        }

        value = parseInt(strValue);

        curIndex = curIndex + length;
        return value;
    }

    function hexToGeo(length){
        positive = data[curIndex] > 0;

        var vals = data.slice(curIndex + 1, curIndex + length);
        var strValue = '0x';
        for (i in vals) {
            strValue += ('00' + vals[i].toString(16)).slice(-2);
        }
        value = parseInt(strValue) * 1.0 / 10000;

        if (!positive)
            value *= -1;

        curIndex = curIndex + length;
        return value;
    }

    // obj.Lat = hexToGeo(length=5);
    // obj.Long = hexToGeo(length=5);
    obj.Date = hexToInt(length=4);
    obj.Confirmed = hexToInt(length=3);
    obj.Deaths = hexToInt(length=3);
    obj.Recovered = hexToInt(length=3);
    obj.Active = hexToInt(length=3);
    return obj;
}

function Decoder(bytes, port) {
  return DecodeCovidPayload(bytes);
}