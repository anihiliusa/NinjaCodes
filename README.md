//==========================================================================================================================
#property copyright "Telegram: @bayUSDT"
#property link  "https://t.me/bayUSDT"   // "WEBSITE"
#property strict
//==========================================================================================================================
extern double LotExponent = 1.11;     // LotExponent                                                     //  умножаване на партиди в серия експоненциално, за да достигнете рентабилност. първа партида 0.1, серия: 0.15, 0.26, 0.43 ...
extern double Lots = 0.01;           // Lots                                                            // микролотове 0.01, докато ако е 0.1, тогава следващият лот в серията ще бъде 0.16
extern int lotdecimal = 2;           // Lotdecimal                                                      // 2 - микро партиди 0,01, 1 - мини партиди 0,1, 0 - нормални партиди 1,0
extern double TakeProfit = 1000.0;   // TakeProfit                                                      // тейк профит
extern double PipStep = 240.0;       // PipStep                                                         // стъпка на коляно
extern double slip = 3.0;            // Slip                                                            //  приплъзване
extern int MaxTrades = 15;           // MaxTrades                                                       // максимален брой едновременно отворени поръчки
extern int MagicNumber = 69;         // MagicNumber                                                     //  магия
extern double TotalEquityRisk = 10;  // MaxRisk
extern bool UseEquityStop = FALSE;    // MaxRisk YES/NO
extern bool UseTrailingStop = true;
extern bool UseTimeOut = FALSE;
extern double MaxTradeOpenHours = 48.0;
extern double Stoploss   = 100;
extern double TrailStart = 100;
extern double TrailStop  = 54;
extern bool TradeNow = FALSE, LongTrade = FALSE, ShortTrade = FALSE;
extern bool NewOrdersPlaced = FALSE;






//+------------------------------------------------------------------+

