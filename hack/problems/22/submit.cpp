      
#include<bits/stdc++.h>
using namespace std;

int search(int arr[], int n,int key){
    /* Write your code here */
   for(int i=0;i<n;i++){
if(arr[i]==key)
   return i;
}
return -1;
}
int main(int argc, char const *argv[])
{
    int t;
    int n;
    int key;
    int *arr = 0;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>n;
    arr = new int[n];
    for(int j=0;j<n;j++)
        cin>>arr[j];
    cin>>key;
    result = search(arr,n,key);
    cout<<result<<endl; 
    delete[] arr;
    }
 	
 	
 	return 0;
} 

    