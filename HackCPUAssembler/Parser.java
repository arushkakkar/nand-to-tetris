import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;


public class Parser {

    private File f;
    private Scanner s;
    private String code;
    private char type;

    public Parser(String path) throws FileNotFoundException{
        f = new File(path);
        s = new Scanner(f);
    }

    public String[] parseNext() throws Exception{
        if(s.hasNext()){
            code = s.nextLine();
            while(code.substring(0, 2).equals("//") || code.equals("\n")){
                if(s.hasNext()){
                    code = s.nextLine();
                }
                else{
                    return null;
                }
            }

            int comment = code.indexOf("//");
            if(comment!= -1){
                code = code.substring(0, comment);
            }

            code.replaceAll("\\s+", "");
            //System.out.println(code.length());

            type = instructionType();
            String destination = getDestination();
            String operation = getALUOperation();
            String jump = getJumpOperation();
            String symbol = getSymbol();
            
            return new String[]{Character.toString(type), destination, operation, jump, symbol};
        }
        s.close();
        return null;
    }

    private char instructionType(){
        char charAt0 = code.charAt(0);
        if(charAt0 == '@')
            return 'A';
        if(charAt0 == '(')
            return 'L';
        return 'C';
    }

    private String getDestination(){
        if(type == 'C'){
            int eq = code.indexOf('=');
            if(eq != -1)
                return code.substring(0, eq);
        }
        return "null";
    }

    private String getALUOperation(){
        if(type == 'C'){
            int  eq = code.indexOf('=');
            int semi = code.indexOf(';');

            if (eq != -1 && semi != -1)
                return code.substring(eq+1, semi);
            else if (eq != -1 && semi == -1)
                return code.substring(eq+1, code.length());
            else if (eq == -1 && semi != -1)
                return code.substring(0, semi);
            else if (eq == -1 && semi == -1)
                return code;
        }
        return "null";
    }

    private String getJumpOperation(){
        if(type == 'C'){
            int semi = code.indexOf(';');
            if(semi != -1)
                return code.substring(semi+1, code.length());
        }
        return "null";
    }

    
    private String getSymbol(){
        if(type == 'A')
            return code.substring(1, code.length());
        if(type == 'L')
            return code.substring(1, code.length()-1);
        return "null";
    }
}