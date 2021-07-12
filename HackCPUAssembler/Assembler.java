import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

class Assembler {
    public static void main(String[] args){
        String[] filePaths = new String[]{
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\add\\Add.asm",
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\max\\Max.asm",
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\rect\\Rect.asm",
            "C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\pong\\Pong.asm"
        };
        Assembler assembler = new Assembler();
        try {
            FileWriter fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\add\\Add.hack");
            fw.write(assembler.assemble(filePaths[0]));
            fw.close();

            fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\max\\Max.hack");
            fw.write(assembler.assemble(filePaths[1]));
            fw.close();

            fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\rect\\Rect.hack");
            fw.write(assembler.assemble(filePaths[2]));
            fw.close();

            fw = new FileWriter("C:\\Users\\aroos\\Desktop\\School\\3650\\nand2tetris\\projects\\06\\pong\\Pong.hack");
            fw.write(assembler.assemble(filePaths[3]));
            fw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String signExtend(String c){
        String s = "";
        for(int i = 0; i < 15 - c.length(); i++)
            s += "0";
        return s + c;
    }

    public String assemble(String path){
        String s = "";

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

        int instructionCounter = 0;
        int ramAddress = 16;
        while (true){
            instructionCounter++;
            try{
                String[] temp = parser.parseNext();
                if(temp[0].charAt(0) == 'L'){
                    instructionCounter--;
                    SymbolTable.add(temp[4], instructionCounter);
                }
            }
            catch(Exception e){
                try{
                parser = new Parser(path);
                }
                catch(FileNotFoundException e2){}
                break;
            }
        }
        while (true){
            try{
                String[] temp = parser.parseNext();
                if(temp[0].charAt(0) == 'A'){
                    try{
                        if(symbols.contains(temp[4]))
                            continue;
                        Integer.parseInt(temp[4]);
                    }
                    catch(NumberFormatException e){
                        SymbolTable.add(temp[4], ramAddress);
                        ramAddress++;
                    }
                }
            }
            catch(Exception e){
                try{
                parser = new Parser(path);
                }
                catch(FileNotFoundException e2){}
                break;
            }
        }
        while(true){
            String[] details;
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
                     s += "0" + signExtend(Integer.toBinaryString(address)) + "\n";
                }

                if(type == 'C'){
                    String instruction = "111";
                    instruction += decoder.getComp(details[2]) + decoder.getDest(details[1]) + decoder.getJump(details[3]);
                    s += instruction + "\n";
                }

                if(type == 'L'){
                    continue;
                }

            }
            catch(Exception e){
                break;
            }
        }
        return s;
    }
}