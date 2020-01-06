//
//  fuke_encrypter.cpp
//  
//
//  Created by Shoma on 12/12/19.
//

#include <stdio.h>
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <initializer_list>
using namespace std;


long encrypt(int x, long key, long p) // encryption algorithm
{
    long z;
    z = (key * x) % p;
    return z;
}

char decrypt(long x, long key, long p) // decryption algorithm
{
    for (long i = 32; i < 127;i++)
    {
        if ((i*key) % p == x)
        {
            return static_cast<char>((int)i);
        }
        else {;}
    }
}

long key2int(char key[13]) // convert password into integer
{
    long keyint = 0;
    for (int i = 0; i < 5; i++)
    {
        long ia = (int)key[i];
        keyint = 1000 * keyint + (ia + 80);
    }
    for (int i = 5; i < strlen(key); i++)
    {
        int ia = (int)key[i];
        keyint = keyint + ia;
    }
    return keyint;
        
}

int initializer() // prompts startup
{
    int response;
    cout << "\nEnter 1 to encrypt, 0 to decrypt, or 2 to exit.\n";
    cin >> response;
    if ((response < 0) or (response > 2))
    {
        cout << "Please enter 1 or 2 or 0!\n";
        response = initializer();
        return response;
    }
    else
        return response;
}



int main()
{
    long p;
    p = 44560482149;
    string words;
    char key[13];
    cout << "Welcome to Shoma's encryption program! \nVersion 1.2.1 \n\n";
    int response;
    response = initializer();
    if (response == 1)//encryption
    {
        string input_file_name;
        cout<<"\nPlease input the name of file (with extension e.g., input_file.txt) you wish to encrypt: ";
        cin >> input_file_name;
        cout << "\n";
        ifstream myfile;
        myfile.open (input_file_name.c_str());
        if (myfile.is_open())//file exists
        {
            cout<<"\nFile found!\n";

            cout << "Please enter a key (password) to use for this encryption (min 6 characters, max 12 characters): ";
            cin >> key;
            cout << "\n";
            long keyint; // password
            keyint = key2int(key); // password as an integer
            
            string ouput_file_name;
            cout<<"\nPlease name the output file (with extension e.g., encrypted_file.txt) you wish to encrypt: ";
            cin >> ouput_file_name;
            
            fstream myoutfile (ouput_file_name.c_str(),ios::app);
            
            cout << "\n";

            string words;
            while (getline(myfile,words))
            {
                //cout << line << '\n';

                vector<char> word(words.begin(),words.end());
                for (int i = 0; i < (int) word.size(); i++)
                {
                    long ia;
                    ia = encrypt((int)word.at(i), keyint, p); // encryption happens here
                    if (myoutfile.is_open())
                    {
                        if (i < (((int) word.size() )- 1))
                        myoutfile << ia <<",";
                        else myoutfile << ia;
                    }
                    else
                    {
                        cout<<"Cannot write to output file!";
                        try
                         {
                             int temp;
                             temp = main();
                         }
                         catch (...){return 0;}
                    }
                }
                myoutfile << "\n";
            }
            myfile.close();
            myoutfile.close();
            cout<<"Encryption complete!\n\n";
            return 0;
        
            
            
        }
        else//file does NOT exist
        {
            cout<<"\nCannot find file! Please make sure you have the right file name.\n";
            try
            {
                int temp;
                temp = main();
            }
            catch (...){return 0;}
            
        }
    }
    
    
    
    else if (response == 0)//decryption
    {
        string input_file_name2;
        cout<<"\nPlease input the name of file (with extension e.g., input_file.txt) you wish to encrypt: ";
        cin >> input_file_name2;
        cout << "\n";
        
        ifstream myfile2;
        myfile2.open (input_file_name2.c_str());
        
        if (myfile2.is_open())//file exists
        {
            cout << "\nFile found!\n";
            char key2[13];
            cout << "Please enter your password: ";
            cin >> key2;
            cout << "\n\nAttempting to decrypt with given password now...\n\n\n";
            long keyint2;
            keyint2 = key2int(key2);
            
            string line;
            while (std::getline(myfile2,line)) // loop through lines of the chosen text file
            {
                if (line.empty())
                {
                    cout<<"\n";
                }
                else
                {
                    vector<long> dline;
                    stringstream ss(line);
                    while (ss.good())
                    {
                        string::size_type sz;
                        string substr;
                        getline(ss, substr, ',');
                        dline.push_back(stol(substr,&sz));
                    }
                    //cout << dline;
                    for (int i = 0; i < (int) dline.size(); i++) // loop through characters in this line
                    {
                        char ia;
                        ia = decrypt(dline.at(i),keyint2,p); // decryption happens here
                        cout<<ia;//<<"\n";
                    }
                    cout << "\n";
                }
            }
        }
        else//file does NOT exist
        {
            cout<<"\nCannot find file! Please make sure you have the right file name.\n";
            try
            {
                int temp;
                temp = main();
            }
            catch (...){return 0;}
        }
    }
    else if (response == 2)
    {
        cout << "\n\nDone!\n\n";
        return 0;
    }
    else
    {
        cout <<"Fatal error! Attempting to restart...\n\n";
        try
        {
            int temp;
            temp = main();
        }
        catch (...){return 0;}
    }
    cout << "\n\nDone!\n\n";
    return 0;
}

