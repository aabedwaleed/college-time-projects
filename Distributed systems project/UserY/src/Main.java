import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Main {
    public static void main(String[] args) throws IOException {
            ServerSocket server=new ServerSocket(8888);
            System.out.println("Server started");
            Socket serverClient=server.accept();
            System.out.println("Client connected");
            Thread1 t = new Thread1(serverClient);
            t.run();
    }
}