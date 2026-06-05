// lib/main.dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Simulasi data sensitif yang akan dicetak ke log
    String userEmail = "mahasiswa@umm.ac.id";
    String authToken = "abc-123-xyz-secret";

    // Memicu temuan (Ini akan tertangkap oleh skrip Python kita)
    print("User email: $userEmail"); 
    debugPrint("Auth Token: $authToken");

    // Kode yang aman (Tidak memicu temuan)
    print("Aplikasi dimulai dengan aman");

    return const MaterialApp(home: Scaffold(body: Center(child: Text("Test Privasi"))));
  }
}