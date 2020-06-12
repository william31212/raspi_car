//宣告變數
int Lspeed;
int Rspeed;
int Ldirection;
int Rdirection;

void setup() {
//給變數相應腳位
  Serial.begin(9600);
  Lspeed = 5;
  Rspeed = 6;
  Ldirection = 8;
  Rdirection = 9;

  pinMode(Ldirection, OUTPUT);
  pinMode(Rdirection, OUTPUT);
}
//
typedef unsigned char uint_8;
typedef struct attr_t {
    uint_8 ldir;
    uint_8 lspeed;
    uint_8 rdir;
    uint_8 rspeed;
}Attr;
typedef union ins
{
  uint_8 buf[4];
  Attr attr;
}Ins;

void loop() {
  if(Serial.available())
  {
    Ins in;
    Serial.readBytes((char*)in.buf, 4);
    char buf[32];
    sprintf(buf, "Receive: %c %d %c %d\n", in.attr.ldir, in.attr.lspeed, in.attr.rdir, in.attr.rspeed);
    Serial.print(buf);
    //
    char ldir = in.attr.ldir, rdir = in.attr.rdir, lspeed = in.attr.lspeed, rspeed = in.attr.rspeed;

    digitalWrite(Ldirection, ldir == '+' ? LOW : HIGH);
    digitalWrite(Rdirection, rdir == '+' ? LOW : HIGH);
    analogWrite(Lspeed, lspeed);
    analogWrite(Rspeed, rspeed);
  }
}
