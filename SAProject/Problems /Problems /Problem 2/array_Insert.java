/* IMPORTANT: Multiple classes and nested static classes are supported */
 
/*
 * uncomment this if you want to read input.
//imports for BufferedReader
import java.io.BufferedReader;
import java.io.InputStreamReader;
 
//import for Scanner and other utility classes
import java.util.*;
*/
 
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.*;
 
// Warning: Printing unwanted or ill-formatted data to output will cause the test cases to fail
 
class TestClass {
   public static int[] arr;
	public static int[] cumulative;
	public static int[] update;
	
	public static void main(String args[] ) throws Exception {
		
		FastReader scan = new FastReader();
		BufferedWriter log = new BufferedWriter(new OutputStreamWriter(System.out));
		
		int N = scan.nextInt();
		int Q = scan.nextInt();
		
		arr = new int[N];
		cumulative = new int[N];
		update = new int[N];
		
		int val = 0;
		for(int i = 0; i<N; i++) {
			arr[i] = scan.nextInt();
			val += arr[i];
			cumulative[i] = val;
		}
		
		int a, b, c;
		for(int i = 0; i<Q; i++) {
			a = scan.nextInt();
			if(a == 1) {
				update(scan.nextInt(), scan.nextInt());
//				printArray(arr);
//				printArray(update);
			} else if(a == 2) {
				int ans = sum(scan.nextInt(), scan.nextInt());
				log.write(ans+"\n");
			}
				
		}
		
		log.flush();
		
	}
 
	// update
	private static void update(int pos, int val) {
		int temp = arr[pos];
		arr[pos] = val;
		update[pos] += (val - temp);
		
	}
 
	// sum
	private static int sum(int start, int end) {
		int sum = -1;
		if(start > 0)
			sum = cumulative[end] - cumulative[start-1];
		else
			sum = cumulative[end];
		
		for(int i = start; i <= end; i++)
			sum += update[i];
		
		return sum;
	}
	
	 private static void printArray(int[] anArray) {
	      for (int i = 0; i < anArray.length; i++) {
	         if (i < anArray.length-1) {
	            System.out.print(anArray[i]+", ");
	         }else
	        	 System.out.println(anArray[i]);
	      }
	   }
	
}
 
 
 
class FastReader {
    BufferedReader br;
    StringTokenizer st;
 
    public FastReader() {
        br = new BufferedReader(new
                 InputStreamReader(System.in));
    }
 
    String next() {
        while (st == null || !st.hasMoreElements())
        {
            try
            {
                st = new StringTokenizer(br.readLine());
            }
            catch (IOException  e)
            {
                e.printStackTrace();
            }
        }
        return st.nextToken();
    }
 
    int nextInt() {
        return Integer.parseInt(next());
    }
    
 
    long nextLong() {
        return Long.parseLong(next());
    }
 
    double nextDouble() {
        return Double.parseDouble(next());
    }
 
    String nextLine() {
        String str = "";
        try
        {
            str = br.readLine();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return str;
    }
    
}