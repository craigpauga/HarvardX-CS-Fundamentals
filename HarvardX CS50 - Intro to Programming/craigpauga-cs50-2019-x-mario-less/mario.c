// Craig Pauga
// 15 May 2019
// Problem Set 1

//Create # pyramid from Mario
#include <cs50.h>
#include <stdio.h>

//Declaring function
void mario(void);

//Create # pryamid from Mario
int main(int argc, string argv[])
{
    mario();
}

void mario(void)
{
    //Initialize height
    int n;
    
    //Obtain user input
    do
    {
        n = get_int("Height: ");            
    } 
    while (n <= 0 || n > 8);
    
    //Outer Loop
    for (int i = 1; i <  n + 1; i++)
    {
        //Inner Loop        
        for (int j = 1; j < n + 1; j++)
        {
            //Check if space or #
            if (j > n - i)
            {
                printf("#");
            } 
            else
            {
                printf(" "); 
            }
             
        }
        printf("\n");
    }
}
