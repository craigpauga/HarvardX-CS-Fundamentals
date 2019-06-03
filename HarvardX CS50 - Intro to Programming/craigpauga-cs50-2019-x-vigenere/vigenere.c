//Craig Pauga
//May 15 2019
//CS50

//Program to encrypt message
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

//Declaration of encryption method
string Encrypt(string plaintext, string keyword);

int main(int argc, string argv[])
{
    //Initialize c and p
    char c;
    char p;

    //Make sure only one input
    if (argc == 2)
    {
        //Make sure that input in fully alphabetic
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if ((argv[1][i] >= 'a' && argv[1][i] <= 'z') || (argv[1][i] >= 'A' && argv[1][i] <= 'Z'))
            {
                continue;
            }
            else
            {
                //Print correct instructions
                printf("Usage: ./caesar keyword\n");
                return 1;
            }
        }
        //String to Int
        string keyword = argv[1];

        //Get User String
        string plaintext = get_string("plaintext: ");

        //Encrypt given String
        string ciphertext = Encrypt(plaintext, keyword);

        //Print new cipher
        printf("ciphertext: %s\n", ciphertext);

        return 0;
    }
    else
    {
        //Print correct instructions
        printf("Usage: ./caesar keyword");
        return 1;
    }
}

string Encrypt(string plaintext, string keyword)
{
    //counter for letters
    int count = 0;
    
    //n is length of string
    int n = strlen(plaintext);
    
    //k_len is length of keyword
    int k = strlen(keyword);
    
    //Iterate through string
    for (int i = 0; i < n; i++)
    {   
        //Get key from keyword     
        int j = count % k;      
        char char_keyword = keyword[j];
        char_keyword = toupper(char_keyword);
        int key = (int) char_keyword - 'A';
        
        
        //Get Character
        char p = plaintext[i];

        //Convert char to int
        int c_int = ((int) p + key);

        //Consider lower case
        if (p >= 'a' && p <= 'z')
        {   
            //Consider rotation
            if (c_int > 'z')
            {
                c_int = (c_int - 'a') % 26 + 'a';
            }
            count++;

        }
        //Consider upper case
        else if (p >= 'A' && p <= 'Z')
        {
            //Consider Rotation
            if (c_int > 'Z')
            {
                c_int = (c_int - 'A') % 26 + 'A';
            }
            count++;
        }
        else
        {
            continue;
        }

        //Convert from Int to String
        char c = (char)(c_int);
        //Change char in string to new char
        plaintext[i] = c;

    }
    return plaintext;
}
