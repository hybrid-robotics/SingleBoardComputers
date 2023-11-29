#include <LiquidCrystal.h>

/*
  Connections:
    rs (LCD pin 4) to Arduino pin 8
    rw (LCD pin 5) to Arduino pin 9
    LCD pins d4, d5, d6, d7 to Arduino pins 4, 5, 6, 7
*/
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  int backLight = 3;                //  Pin 3 will control the backlight 
  pinMode(backLight, OUTPUT);       //  Make it an output
  analogWrite(backLight, 50);       //  Set the baklight value

  /*
    DOG-M - this is required to initialise the
      LCD on the Firewing LCD+ shield...
  */
  lcd.command(0x29);                //  4 bit interface
  lcd.command(0x1C);                //  Bias set 
  lcd.command(0x52);                //  Power control
  lcd.command(0x69);                //  Follower control
  lcd.command(0x74);                //  Set contrast
  lcd.command(0x38);                //  Function set
  /*
    END DOG-M 
  */

  lcd.begin(16,3);                  //  Columns, Rows.  use 16,3 for a 16x3 LCD

  lcd.clear();                  
  lcd.setCursor(0, 0);           
  lcd.print("Firewing");   
  lcd.setCursor(0, 1);
  lcd.print("elapsed : ");

  //  Some extra data for 3 line LCD...
  lcd.setCursor(0, 2);              //  Set cursor to column 0, row 0 (the first row) 
  lcd.print("3 line LCD!");         //  Change this text to whatever you like. keep it clean.
}

// main program loop...
void loop(void) {
  lcd.setCursor(10, 1);
  lcd.print(millis()/1000);
} 