/*
 * Decompiled with CFR 0.138.
 */
package hackvent2018.pills;

import hackvent2018.pills.Cipher3;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.StandardOpenOption;
import java.nio.file.Path;

public class Solve {
    public static void main(String[] args) throws IOException {
        int num1, num2, num3;
        String serial_num = "";
        for (num1 = 0; num1 < 100; num1++) {
            for (num2 = 0; num2 < 1000; num2++) {
                for (num3 = 0; num3 < 1000; num3++) {
                    serial_num = String.format("%02d-%03d-%03d", num1, num2, num3);
                    //System.out.println(serial_num);
                    brute(serial_num);
                }
            }
            System.out.println("Status: " + serial_num);
        }

    }
    public static void solve(String serial_number) throws IOException {
        // Format of serial is NN-NNN-NNN (where N is 0-9)
        if (!serial_number.matches("[0-9]{2}-[0-9]{3}-[0-9]{3}")) {
            System.out.println("That's not a red pill");
            System.exit(0);
        }
        // Create initialization vector based on user input
        byte[] iv = serial_number.replace("-", "").getBytes();

        // Key size is 16 bytes
        byte[] k = new byte[16];

        // Format of array copy is: source_arr, source_pos, dest_arr, dest_pos, len
        // Thus the key is the serialnum + serialnum (string concatenation)
        System.arraycopy(iv, 0, k, 0, 8);
        System.arraycopy(iv, 0, k, 8, 8);

        // Read the flag file
        byte[] b = Files.readAllBytes(new File("flag_encrypted").toPath());


        // Create cipher
        Cipher3 c = new Cipher3();

        // Set up key
        c.setupKey(k);

        // Set up initialization veector
        c.setupIV(iv);


        // Encrypt the halfed byte stream
        byte[] fd = c.crypt(b); // Half the size

        byte[] f = new byte[(fd.length * 2)]; // Double the size

        for (int i = 0; i < f.length; i+=2) {
            f[i]   = (byte)((fd[i/2] >> 4) & 0xf | 0x40);
            f[i+1] = (byte)((fd[i/2] & 0xf) | 0x40);
        }
        byte[] out = new byte[20]; // limit
        for (int i = 0; i < out.length; i++) {
            out[i]   = f[i];
        }
        /*
        System.out.print("fd = ");
        for (int i = 0; i < fd.length; i++) {
            String st = String.format("%02X", fd[i]);
            System.out.print(st);
        }
        System.out.println();
        System.out.print("f = ");
        for (int i = 0; i < f.length; i++) {
            String st = String.format("%02X", f[i]);
            System.out.print(st);
        }
        */
        //System.out.println();
        //Files.write(new File("solver").toPath(), f, new OpenOption[0]);
        Files.write(new File("solver").toPath(), serial_number.getBytes(), StandardOpenOption.APPEND);
        String colon = ": ";
        Files.write(new File("solver").toPath(), colon.getBytes(), StandardOpenOption.APPEND);
        Files.write(new File("solver").toPath(), out, StandardOpenOption.APPEND);
        String newline = "\n";
        Files.write(new File("solver").toPath(), newline.getBytes(), StandardOpenOption.APPEND);
    }
    public static void brute(String serial_number) throws IOException {
        // Format of serial is NN-NNN-NNN (where N is 0-9)
        if (!serial_number.matches("[0-9]{2}-[0-9]{3}-[0-9]{3}")) {
            System.out.println("That's not a red pill");
            System.exit(0);
        }
        // Create initialization vector based on user input
        byte[] iv = serial_number.replace("-", "").getBytes();

        // Key size is 16 bytes
        byte[] k = new byte[16];

        // Format of array copy is: source_arr, source_pos, dest_arr, dest_pos, len
        // Thus the key is the serialnum + serialnum (string concatenation)
        System.arraycopy(iv, 0, k, 0, 8);
        System.arraycopy(iv, 0, k, 8, 8);

        // Read the flag file
        // Known plaintext:  8950 4e47 0d0a 1a0a 0000 000d 4948 4452
        // (From header of PNG file)
        byte[] b = { (byte)0x89, (byte)0x50,
                     (byte)0x4e, (byte)0x47,
                     (byte)0x0d, (byte)0x0a,
                     (byte)0x1a, (byte)0x0a,
                     (byte)0x00, (byte)0x00,
                     (byte)0x00, (byte)0x0d,
                     (byte)0x49, (byte)0x48,
                     (byte)0x44, (byte)0x52
        };

        // Known plaintext: flag_encrypted.orig 1ed5 3bf4 6f3f ad6b 3895 ca65 811b ea58

        // This is a little strange
        // Best way to explain is by example:
        // if input is 0x41, 0x41, 0x42, 0x42:
        // Create a byte stream of the lower four bits
        // output is 0x11, 0x22
        byte[] f = new byte[(b.length + 1) / 2];

        for (int i = 0; i < b.length; ++i) {
            f[i / 2] = i % 2 == 0 ? (byte)(f[i / 2] | b[i] << 4) : (byte)(f[i / 2] | b[i] & 15);
        }

        // Create cipher
        Cipher3 c = new Cipher3();

        // Set up key
        c.setupKey(k);

        // Set up initialization veector
        c.setupIV(iv);

        // Encrypt the halfed byte stream
        byte[] fc = c.crypt(f);
        //Files.write(new File("flag_encrypted").toPath(), fc, new OpenOption[0]);
        // Known ciphertext: 59c5 b2ab 1af2 abbc
        // 59 c5 b2 ab 1a f2 ab bc
        if (fc[0] == (byte)(0x59) && fc[1] == (byte)(0xc5) &&
            fc[2] == (byte)(0xb2) && fc[3] == (byte)(0xab) &&
            //fc[4] == (byte)(0x1a) && fc[5] == (byte)(0xf2) &&
            //fc[6] == (byte)(0xab) && fc[7] == (byte)(0xbc)
            true
           ) {
           //System.out.println(serial_number);
            String fc0;
            String fc1;

            fc0 = String.format("%02X", fc[0]);
            fc1 = String.format("%02X", fc[1]);
            System.out.println("[+] " + serial_number + ":" + fc0 + fc1 );
        }
    }
}
