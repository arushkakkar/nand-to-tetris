import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

class AssemblerNoSymbols {
    public static void main(String[] args){
        String[] filePaths = new String[]{
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\max\\MaxL.asm",
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\rect\\RectL.asm",
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\pong\\PongL.asm"
        };
        Assembler assembler = new Assembler();
        try {
            FileWriter fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\max\\MaxL.hack");
            fw.write(assembler.assemble(filePaths[0]));
            fw.close();

            fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\rect\\RectL.hack");
            fw.write(assembler.assemble(filePaths[1]));
            fw.close();

            fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\pong\\PongL.hack");
            fw.write(assembler.assemble(filePaths[2]));
            fw.close();
        }
        catch(IOException e){
            e.printStackTrace();
        }
    }

    private String signExtend(String c){
        String s = "";
        for(int i = 0; i < 15 - c.length(); i++)
            s += "0";
        return s + c;
    }

    public void assemble(String path){
        Parser parser = null;
        try{
            parser = new Parser(path);
        }
        catch(FileNotFoundException e){
            e.printStackTrace();
            System.exit(0);
        }
        DecodeCType decoder = new DecodeCType();
        SymbolTable symbols = new SymbolTable();

        while(true){
            String details[];
            try{
            details = parser.parseNext();
            char type = details[0].charAt(0);

            if(type == 'A'){
                int address;
                try{
                    address = Integer.parseInt(details[4]);
                }
                catch(NumberFormatException e){
                    address = symbols.getAddress(details[4]);
                }
                System.out.println("0" + signExtend(Integer.toBinaryString(address)));
            }

            if(type == 'C'){
                String instruction = "111";
                instruction += decoder.getComp(details[2]) + decoder.getDest(details[1]) + decoder.getJump(details[3]);
                System.out.println(instruction);
            }

            }
            catch(Exception e){
                break;
            }
        }
    }
}