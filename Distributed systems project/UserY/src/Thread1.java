import java.io.*;
import java.net.Socket;

public class Thread1 {
    Socket s;


    public Thread1(Socket s) {
        this.s = s;
    }

    public void run() throws IOException {
        DataInputStream inStream=new DataInputStream(s.getInputStream());
        DataOutputStream outStream=new DataOutputStream(s.getOutputStream());
        BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
        String clientMessage="",serverMessage = "";
        while(!clientMessage.equals("bye")){
            clientMessage=br.readLine();
            outStream.writeUTF(clientMessage);
            outStream.flush();
            serverMessage=inStream.readUTF();
            System.out.println("From Server: "+serverMessage);
        }
        outStream.close();
        outStream.close();
        s.close();
    }
}