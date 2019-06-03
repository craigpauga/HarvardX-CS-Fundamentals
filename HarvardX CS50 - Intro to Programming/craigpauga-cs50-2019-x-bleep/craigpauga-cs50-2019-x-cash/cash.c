// Craig Pauga
// 15 May 2019
// Problem Set 1

//Get the amount of change owed
#include <cs50.h>
#include <stdio.h>
#include <math.h>

//Declare cash function
void cash(void);

//Get the amount of change owed
int main(int argc, string argv[])
{
    cash();
}

void cash(void)
{
    //Initialize the change amount 
    float change;
    int n = 0;
    
    //Obtain User Input
    do
    {
        change = get_float("Change owed: ");       
    } 
    while (change <= 0);
    
    //Turn float to int
    int cash = round(change * 100);
    
    //While Loop that chips away at change until negative
    while (cash > 0)
    {   
        //Representing a quarter
        if (cash >= 25)
        {
            cash -= 25;
            n++;
        }
        //Representing a dime
        else if (cash < 25 && cash >= 10)
        {
            cash -= 10;
            n++;
        }
        //Representing a nickel
        else if (cash < 10 && cash >= 05)
        {
            cash -= 05;
            n++;
        }
        //Representing a penny
        else
        {
            cash -= 01;
            n++;
        }
    }
    //Print the answer
    printf("%i\n", n);
}
