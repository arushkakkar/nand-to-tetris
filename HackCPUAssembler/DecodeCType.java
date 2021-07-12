import java.util.HashMap;
import java.util.Map;

class DecodeCType{

    Map<String, String> dMap = new HashMap<String, String>();
    Map<String, String> cMap = new HashMap<String, String>();
    Map<String, String> jMap = new HashMap<String, String>();

    public DecodeCType(){
        dMap.put("null", "000");
        dMap.put("M", "001");
        dMap.put("D", "010");
        dMap.put("MD", "011");
        dMap.put("A", "100");
        dMap.put("AM", "101");
        dMap.put("AD", "110");
        dMap.put("AMD", "111");

        cMap.put("null", "0000000");
        cMap.put("0", "0101010");
        cMap.put("1", "0111111");
        cMap.put("-1", "0111010");
        cMap.put("D", "0001100");
        cMap.put("A", "0110000");
        cMap.put("!D", "0001101");
        cMap.put("!A", "0110001");
        cMap.put("-D", "0001111");
        cMap.put("-A", "0110011");
        cMap.put("D+1", "0011111");
        cMap.put("A+1", "0110111");
        cMap.put("D-1", "0001110");
        cMap.put("A-1", "0110010");
        cMap.put("D+A", "0000010");
        cMap.put("D-A", "0010011");
        cMap.put("A-D", "0000111");
        cMap.put("D&A", "0000000");
        cMap.put("D|A", "0010101");
        cMap.put("M", "1110000");
        cMap.put("!M", "1110001");
        cMap.put("-M", "1110011");
        cMap.put("M+1", "1110111");
        cMap.put("M-1", "1110010");
        cMap.put("D+M", "1000010");
        cMap.put("D-M", "1010011");
        cMap.put("M-D", "1000111");
        cMap.put("D&M", "1000000");
        cMap.put("D|M", "1010101");

        jMap.put("null", "000");
        jMap.put("JGT", "001");
        jMap.put("JEQ", "010");
        jMap.put("JGE", "011");
        jMap.put("JLT", "100");
        jMap.put("JNE", "101");
        jMap.put("JLE", "110");
        jMap.put("JMP", "111");
    }

    public String getDest(String s){
        return dMap.get(s);
    }

    public String getComp(String s){
        return cMap.get(s);
    }

    public String getJump(String s){
        return jMap.get(s);
    }
}