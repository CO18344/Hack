      
#include<bits/stdc++.h>
using namespace std;

void reverse(int arr[], int n){
    /* Write your code here */
    int l = 0;
   int h = n - 1;

while(l<h){
int t = arr[l];
arr[l] = arr[h];
arr[h] = t;

l++;
h--;
}

}
int main(int argc, char const *argv[])
{
    int t;
    int n;
    int *arr = 0;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>n;
    arr = new int[n];
    for(int j=0;j<n;j++)
        cin>>arr[j];
    reverse(arr,n);
    for(int j=0;j<n;j++)
        cout<<arr[j]<<" ";
    cout<<endl; 
    delete[] arr;
    }
 	
 	
 	return 0;
} 

    