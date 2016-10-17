#define spiDataPin 10
#define slaveSelectPin 11
#define spiClockPin 12
#define rssiPin A6

#define CHANNEL_BAND_SIZE 8
#define CHANNEL_MIN_INDEX 0
#define CHANNEL_MAX_INDEX 39

#define CHANNEL_MAX 39
#define CHANNEL_MIN 0

// RSSI default raw range
#define RSSI_MIN_VAL 60
#define RSSI_MAX_VAL 250

unsigned long time_of_tune = 0;        // will store last time when tuner was changed
uint8_t channel = 0;
uint8_t last_channel_index = -1;
uint8_t channelIndex = 24;
uint8_t rssi = 0;
uint8_t rssi_scaled = 0;
uint8_t hight = 0;
//uint8_t state = START_STATE;
//uint8_t state_last_used=START_STATE;
//uint8_t last_state= START_STATE+1; // force screen draw

int state = 0;

uint16_t rssi_min=60;
uint16_t rssi_max=250;

// Channels to sent to the SPI registers
const uint16_t channelTable[] PROGMEM = {
  // Channel 1 - 8
  0x2A05,    0x299B,    0x2991,    0x2987,    0x291D,    0x2913,    0x2909,    0x289F,    // Band A
  0x2903,    0x290C,    0x2916,    0x291F,    0x2989,    0x2992,    0x299C,    0x2A05,    // Band B
  0x2895,    0x288B,    0x2881,    0x2817,    0x2A0F,    0x2A19,    0x2A83,    0x2A8D,    // Band E
  0x2906,    0x2910,    0x291A,    0x2984,    0x298E,    0x2998,    0x2A02,    0x2A0C,    // Band F / Airwave
  0x281D,    0x288F,    0x2902,    0x2914,    0x2987,    0x2999,    0x2A0C,    0x2A1E     // Band C / Immersion Raceband // R
};

// Channels with their Mhz Values
const uint16_t channelFreqTable[] PROGMEM = {
  // Channel 1 - 8
  5865, 5845, 5825, 5805, 5785, 5765, 5745, 5725, // Band A
  5733, 5752, 5771, 5790, 5809, 5828, 5847, 5866, // Band B
  5705, 5685, 5665, 5645, 5885, 5905, 5925, 5945, // Band E
  5740, 5760, 5780, 5800, 5820, 5840, 5860, 5880,  // Band F / Airwave
  5658, 5695, 5732, 5769, 5806, 5843, 5880, 5917  // Band C / Immersion Raceband
};

// do coding as simple hex value to save memory.
const uint8_t channelNames[] PROGMEM = {
  0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, // Band A
  0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, // Band B
  0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, // Band E
  0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, // Band F / Airwave
  0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8  // Band C / Immersion Raceband
};

// All Channels of the above List ordered by Mhz
const uint8_t channelList[] PROGMEM = {
  19, 18, 32, 17, 33, 16, 7, 34, 8, 24, 6, 9, 25, 5, 35, 10, 26, 4, 11, 27, 3, 36, 12, 28, 2, 13, 29, 37, 1, 14, 30, 0, 15, 31, 38, 20, 21, 39, 22, 23
};


void setup() {
    // SPI pins for RX control
    pinMode (slaveSelectPin, OUTPUT);
    pinMode (spiDataPin, OUTPUT);
    pinMode (spiClockPin, OUTPUT);
    Serial.begin(9600);
    setChannelModule(channelIndex);
    last_channel_index = channelIndex;
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    if (inByte == 'R') {
      state = 1;
    }
    if (inByte == 'S') {
      state = 0;
    }
    if (inByte == 'X') {
      state = 2;
    }
    if (inByte == 'C') {
      int x = 0;
      while (!Serial.available()) {
        
      }
      inByte = Serial.read();
      //Serial.println(inByte);
      x = inByte - '0';
      x = x * 10;
      while (!Serial.available()) {
        
      }
      inByte = Serial.read();
      //Serial.println(inByte);
      x = x + inByte - '0';
      channelIndex = x;
    }
  }
  if (last_channel_index != channelIndex) {
    Serial.print("Channel ");
    Serial.println(channelIndex);
    setChannelModule(channelIndex);
    last_channel_index = channelIndex;
    // keep time of tune to make sure that RSSI is stable when required
    time_of_tune=millis();
  }
  if (state == 1) { // scan and send RSSI
    // put your main code here, to run repeatedly:
    wait_rssi_ready();
    uint16_t x = readRSSI();
    Serial.print("RSSI ");
    Serial.println(x);
    delay(10);
  }
  if (state == 2) { // scan all channels
    scanChannels();
  }
}

void scanChannels() {
  uint8_t i = 0;
  Serial.print("SCAN ");
  for (i = 0; i <= CHANNEL_MAX; i++) {
    setChannelModule(i);
    time_of_tune=millis();
    wait_rssi_ready();
    uint16_t x = readRSSI();
    Serial.print(x);
    if (i < CHANNEL_MAX) {
      Serial.print(" ");
    }
  }
  Serial.println("");
  setChannelModule(channelIndex);
}

uint8_t channel_from_index(uint8_t channelIndex)
{
    uint8_t loop=0;
    uint8_t channel=0;
    for (loop=0;loop<=CHANNEL_MAX;loop++)
    {
        if(pgm_read_byte_near(channelList + loop) == channelIndex)
        {
            channel=loop;
            break;
        }
    }
    return (channel);
}    

void wait_rssi_ready()
{
    // CHECK FOR MINIMUM DELAY
    // check if RSSI is stable after tune by checking the time
    uint16_t tune_time = millis()-time_of_tune;
    // module need >20ms to tune.
    // 30 ms will to a 32 channel scan in 1 second.
    #define MIN_TUNE_TIME 30
    if(tune_time < MIN_TUNE_TIME)
    {
        // wait until tune time is full filled
        delay(MIN_TUNE_TIME-tune_time);
    }
}
        

uint16_t readRSSI() 
{
    uint16_t rssi = 0;
    for (uint8_t i = 0; i < 10; i++) 
    {
        rssi += analogRead(rssiPin);
    }
    rssi=rssi/10; // average

    // Filter glitches
    rssi = constrain(rssi, rssi_min, rssi_max);    //original 90---250
    rssi=rssi-rssi_min; // set zero point (value 0...160)
    rssi = map(rssi, 0, rssi_max-rssi_min , 1, 100);   // scale from 1..100%
    
    return (rssi);
}

void setChannelModule(uint8_t channel)
{
  uint8_t i;
  uint16_t channelData;

  //channelData = pgm_read_word(&channelTable[channel]);
  //channelData = channelTable[channel];
  channelData = pgm_read_word_near(channelTable + channel);

  // bit bash out 25 bits of data
  // Order: A0-3, !R/W, D0-D19
  // A0=0, A1=0, A2=0, A3=1, RW=0, D0-19=0
  SERIAL_ENABLE_HIGH();
  delayMicroseconds(1);  
  //delay(2);
  SERIAL_ENABLE_LOW();

  SERIAL_SENDBIT0();
  SERIAL_SENDBIT0();
  SERIAL_SENDBIT0();
  SERIAL_SENDBIT1();

  SERIAL_SENDBIT0();

  // remaining zeros
  for (i = 20; i > 0; i--)
    SERIAL_SENDBIT0();

  // Clock the data in
  SERIAL_ENABLE_HIGH();
  //delay(2);
  delayMicroseconds(1);  
  SERIAL_ENABLE_LOW();

  // Second is the channel data from the lookup table
  // 20 bytes of register data are sent, but the MSB 4 bits are zeros
  // register address = 0x1, write, data0-15=channelData data15-19=0x0
  SERIAL_ENABLE_HIGH();
  SERIAL_ENABLE_LOW();

  // Register 0x1
  SERIAL_SENDBIT1();
  SERIAL_SENDBIT0();
  SERIAL_SENDBIT0();
  SERIAL_SENDBIT0();

  // Write to register
  SERIAL_SENDBIT1();

  // D0-D15
  //   note: loop runs backwards as more efficent on AVR
  for (i = 16; i > 0; i--)
  {
    // Is bit high or low?
    if (channelData & 0x1)
    {
      SERIAL_SENDBIT1();
    }
    else
    {
      SERIAL_SENDBIT0();
    }

    // Shift bits along to check the next one
    channelData >>= 1;
  }

  // Remaining D16-D19
  for (i = 4; i > 0; i--)
    SERIAL_SENDBIT0();

  // Finished clocking data in
  SERIAL_ENABLE_HIGH();
  delayMicroseconds(1);
  //delay(2);

  digitalWrite(slaveSelectPin, LOW);
  digitalWrite(spiClockPin, LOW);
  digitalWrite(spiDataPin, LOW);
}


void SERIAL_SENDBIT1()
{
  digitalWrite(spiClockPin, LOW);
  delayMicroseconds(1);

  digitalWrite(spiDataPin, HIGH);
  delayMicroseconds(1);
  digitalWrite(spiClockPin, HIGH);
  delayMicroseconds(1);

  digitalWrite(spiClockPin, LOW);
  delayMicroseconds(1);
}

void SERIAL_SENDBIT0()
{
  digitalWrite(spiClockPin, LOW);
  delayMicroseconds(1);

  digitalWrite(spiDataPin, LOW);
  delayMicroseconds(1);
  digitalWrite(spiClockPin, HIGH);
  delayMicroseconds(1);

  digitalWrite(spiClockPin, LOW);
  delayMicroseconds(1);
}

void SERIAL_ENABLE_LOW()
{
  delayMicroseconds(1);
  digitalWrite(slaveSelectPin, LOW);
  delayMicroseconds(1);
}

void SERIAL_ENABLE_HIGH()
{
  delayMicroseconds(1);
  digitalWrite(slaveSelectPin, HIGH);
  delayMicroseconds(1);
}
