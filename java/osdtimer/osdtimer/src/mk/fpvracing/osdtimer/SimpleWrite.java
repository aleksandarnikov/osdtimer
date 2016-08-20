package mk.fpvracing.osdtimer;

import java.io.IOException;
import java.io.OutputStream;
import java.util.Enumeration;

import gnu.io.CommPortIdentifier;
import gnu.io.PortInUseException;
import gnu.io.SerialPort;
import gnu.io.UnsupportedCommOperationException;

public class SimpleWrite {
  static Enumeration portList;
  static CommPortIdentifier portId;
  static String messageString = "-\n\r";
  static SerialPort serialPort;
  static OutputStream outputStream;

  public static void main(String[] args) {
    outputStream = openPort("COM12");

    
    getInfo("192.168.42.1");
    
    sendMessage("-");
    sendMessage("1anikov");

    try {
      Thread.sleep(10000);
    } catch (InterruptedException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    try {
      outputStream.close();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

  private static void getInfo(String string) {
    // TODO Auto-generated method stub
    
  }

  private static void sendMessage(String string) {
    // TODO Auto-generated method stub
    String m = string + "\n\r";
    try {
      outputStream.write(m.getBytes());
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

  private static OutputStream openPort(String string) {
    portList = CommPortIdentifier.getPortIdentifiers();

    System.out.println(portList.hasMoreElements());
    while (portList.hasMoreElements()) {
      System.out.println("inside loop");
      portId = (CommPortIdentifier) portList.nextElement();
      if (portId.getPortType() == CommPortIdentifier.PORT_SERIAL) {
        // if (portId.getName().equals("COM1")) {
        System.out.println(portId.getName());
        if (portId.getName().equals("COM12")) {
          try {
            System.out.println("doit");
            serialPort = (SerialPort) portId.open("SimpleWriteApp", 2000);
          } catch (PortInUseException e) {
            e.printStackTrace();
          }
          try {
            outputStream = serialPort.getOutputStream();
          } catch (IOException e) {
            e.printStackTrace();
          }
          try {
            serialPort.setSerialPortParams(9600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
          } catch (UnsupportedCommOperationException e) {
            e.printStackTrace();
          }

          try {
            Thread.sleep(3000);
          } catch (InterruptedException e) {
            e.printStackTrace();
          }

          // outputStream.flush();
          System.out.println("done");

        }
      }
    }
    return outputStream;
  }
}