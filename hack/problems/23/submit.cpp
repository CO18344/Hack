      
#include<bits/stdc++.h>
using namespace std;

int palindrome(string str){
    /* Write your code here */
   int l = 0;
   int h = str.length() - 1;
   while(l<h){
  if(str[l] != str[h])
return 0;

l++;
h--;
}
return 1;

}
int main(int argc, char const *argv[])
{
    int t;
    string str;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>str;
    result = palindrome(str);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    