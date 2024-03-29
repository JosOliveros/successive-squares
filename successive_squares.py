#----------------------------------------------
#
# author: Jonathan Oliveros
#
#----------------------------------------------

import math
import time
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

class DecimalToBinary:

    def __init__(self):
        """
        Init of DecimalToBinary.
        """
        pass

    def convert_db(self, decimal):
        """
        Converts a decimal number to a binary number.
        """
        lst = []
        num = decimal
        while num > 0:
            lst.append(num % 2) # add remainder to binary digit
            num = math.floor(num / 2) # divide by 2 for next iteration
        lst.reverse() #reverse list to put binary number in correct order
        return lst

class successiveSquares:

    def __init__(self, base, exp, m):
        """Init of SuccessiveSquares.
        params:

        base: the base of the number
        exp: the exponent of the number in question
        m: the number we are modding by
        """
        self.base = base
        self.exp = exp
        self.m = m


    def get_mod(self):
        """
        Uses the successive squares algorithm to reduce very large integers
        mod m.

        returns:

        reduced number mod m
        """
        binary = DecimalToBinary()
        bin_num = binary.convert_db(self.exp)
        num_lst = [] # create a list that holds (base**(2**i)) mod m 
        result = 1
        num_lst.append(self.base)# add base number to list since 2**0 == 1
        for i in range(1,len(bin_num)): # start i at 1 to get rest of the list.
            num_lst.append((num_lst[i - 1]**2 % self.m)) # square the result of the previous number on list and mod m
        num_lst.reverse() # reverse list to match up with binary number list order
        for j in range(0, len(bin_num)):
            if bin_num[j] == 1: #the 1's and 0's are flags to see if the index in num_lst can be multiplied to result 
                result *= num_lst[j]
        return result % self.m # the result is easier to reduce mod m and is congruent to original number
  
def get_times(a, m, exp_lst, time_algo_lst, time_naive_lst):
        for i in range(0, 10000):
            ssq = successiveSquares(a, i, m)
            exp_lst.append(i)
            start_algo = time.perf_counter()
            ssq.get_mod()
            end_algo = time.perf_counter()
            time_algo_lst.append(end_algo - start_algo)
            start_naive = time.perf_counter()
            #Throwaway variable. Ensures that it is not displayed in the web app
            throwaway = a**i % m
            end_naive = time.perf_counter()
            time_naive_lst.append(end_naive - start_naive)      

def main():
    st.write(
    """
    ## Successive Squares
    
    Given that
    """)
    st.latex(r'''a,e,m \in \mathbb{Z}''')
    st.write('then we can solve:')
    st.latex("a^e \, \mod \, m")

    a = st.number_input("Please enter a positive integer for a: ",min_value=0)

    e = st.number_input('Enter a positive integer for e: ',min_value=1)

    m = st.number_input('Enter a positive integer for m: ',min_value=2)

    ssq = successiveSquares(a, e, m)
    start_algo = time.perf_counter()
    end_algo = time.perf_counter()
    st.write('Your result is: ' , str(ssq.get_mod()))
    start_naive = time.perf_counter()
    #Throwaway variable. Ensures that it is not displayed in the web app
    throwaway = a**e % m
    end_naive = time.perf_counter()
    st.write('Using the successive squares algorithm it takes ' , str(end_algo - start_algo)
          + ' seconds. Using the naive way it takes '
          + str(end_naive - start_naive) + ' seconds.')
 
    if st.button('Calculate'):
        time_algo_lst = []
        time_naive_lst = []
        exp_lst = []
        get_times(a, m, exp_lst, time_algo_lst, time_naive_lst)
        
        fig = plt.figure()
        plt.plot(exp_lst, time_algo_lst, label='successive squares')
        plt.plot(exp_lst, time_naive_lst, label='naive')
        plt.xlabel('exponent')
        plt.ylabel('time(seconds)')
        plt.title("Successive squares vs. naive algorithms")
        plt.legend()
        st.pyplot(fig)

if __name__ == "__main__":
    main()
