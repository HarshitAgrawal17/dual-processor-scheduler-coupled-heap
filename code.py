"""
Coupled Heap for 2-Processor Scheduling.

"""

class CoupledHeap:
    """
    A heap over two independent priority axes, X and Y.

    Elements are (id, x_pri, y_pri). Priorities are numbers (ints or floats); larger
    means higher priority. On a tie, the larger id wins, on both axes.
    """

    def __init__(self):
        self.n = 0
        self.heapx = []
        self.heapy = []
        pass


    def enqueue(self, id, x_pri, y_pri):
        """Insert an element. O(log n) worst case."""
        e = {'id' : id , 'x_pri' : x_pri , 'y_pri' : y_pri, 'x_ind': self.n , 'y_ind':self.n}
        self.heapx.append(e)
        self.heapy.append(e)
        self.n += 1
        self._up(self.heapx ,'x_pri' , self.n -1 , 'x_ind')
        self._up(self.heapy ,'y_pri' , self.n -1 , 'y_ind')
        
    
    def _up(self, heap , which_pri , index , which_ind):
        
        # id is the actual id
        # which_pri is string x_pri or y_pri
        # which index represents the string 'x_ind' or 'y_ind'
        c = index
        p = (index-1)//2
        
        while (heap[c][which_pri] , heap[c]['id']) > (heap[p][which_pri] , heap[p]['id']) and c > 0:
            self._swap(heap , c , p , which_ind)
            c = p
            p = (c-1)//2
        
    def _down(self, heap , which_pri , ind , which_ind):
        # which index represents 'x_ind' or 'y_ind'
        p = ind
        c = 2*ind + 1
        if c >= self.n: return
        if (c+1 < self.n) and (heap[c][which_pri] , heap[c]['id']) < (heap[c+1][which_pri] , heap[c+1]['id']):
            c = c+1
        while (heap[c][which_pri] , heap[c]['id']) > (heap[p][which_pri] , heap[p]['id']):
            self._swap(heap , c , p , which_ind)
            p = c
            c = 2*c + 1
            if c >= self.n: return
            if (c+1 < self.n) and (heap[c][which_pri] , heap[c]['id']) < (heap[c+1][which_pri] , heap[c+1]['id']):
                c = c+1                    
        
        
    def _swap(self , heap , ci , pi , which_ind):
        # which index represents 'x_ind' or 'y_ind'
        heap[ci] , heap[pi] = heap[pi] , heap[ci]
        heap[ci][which_ind] = ci
        heap[pi][which_ind] = pi
        
        
    def peekMaxX(self):
        """Max X-priority element as (id, x_pri, y_pri); None if empty. O(1)."""
        if self.n == 0: return None
        else:
            e = self.heapx[0]
            return (e['id'] , e['x_pri'] , e['y_pri'])
        

    def peekMaxY(self):
        """Max Y-priority element as (id, x_pri, y_pri); None if empty. O(1)."""
        if self.n == 0: return None
        else:
            e = self.heapy[0]
            return (e['id'] , e['x_pri'] , e['y_pri'])

    def extractMaxX(self):
        """
        Remove and return the max X-priority element as (id, x_pri, y_pri),
        or None if empty. O(log n) worst case.
        """
        if self.n == 0:
            return None
        elif self.n == 1:
            self.n = 0
            e = self.heapx.pop()
            self.heapy.pop()
            return (e['id'] , e['x_pri'] , e['y_pri'])
            
        else:
            e = self.heapx[0]
            
            #modify heapx
            last = self.heapx.pop()
            last['x_ind'] = 0
            self.heapx[0] = last
            
            
            self.n -= 1
            self._down(self.heapx , 'x_pri' , 0 , 'x_ind')
            
            y_removed_index = e['y_ind']
            
            
            y_rem = self.heapy[y_removed_index]
            y_last = self.heapy.pop()
            
            #if y_removed_index = self.n then no problem, it was the last element
            if y_removed_index < self.n:
                y_last['y_ind'] = y_removed_index
                self.heapy[y_removed_index] = y_last
                self._down(self.heapy , 'y_pri' , y_removed_index , 'y_ind')
                self._up(self.heapy , 'y_pri' , y_removed_index , 'y_ind')
                
            
            
            return (e['id'] , e['x_pri'] , e['y_pri'])
            

    def extractMaxY(self):
        """
        Remove and return the max Y-priority element as (id, x_pri, y_pri),
        or None if empty. O(log n) worst case.
        """
        if self.n == 0:
            return None
        elif self.n == 1:
            self.n = 0
            e = self.heapx.pop()
            self.heapy.pop()
            return (e['id'] , e['x_pri'] , e['y_pri'])
        else:
            e = self.heapy[0]
            
            #modify heapy
            last = self.heapy.pop()
            last['y_ind'] = 0
            self.heapy[0] = last
            
            self.n -= 1
            self._down(self.heapy , 'y_pri' , 0 , 'y_ind')
            
            x_removed_index = e['x_ind']
            
            x_rem = self.heapx[x_removed_index]
            x_last = self.heapx.pop()
            
            #if x_removed_index = self.n then no problem, it was the last element
            if x_removed_index < self.n:
                x_last['x_ind'] = x_removed_index
                self.heapx[x_removed_index] = x_last
                self._down(self.heapx ,'x_pri', x_removed_index , 'x_ind')  
                self._up(self.heapx ,'x_pri', x_removed_index , 'x_ind') 
                
            return (e['id'] , e['x_pri'] , e['y_pri'])



def solve_scheduling(jobs):
    """
    Simulate the two processors and return (total_profit, total_waiting_time).

    jobs: list of (t_i, t0_i, t1_i, p0_i, p1_i), sorted by arrival time t_i.

    Target: O(N log N) time, O(N) space.
    """
    p1 = 0
    p2 = 0
    t = 0
    # p1 and p2 denote when these processors will be free next
    total_profit = 0
    total_time = 0
    
    tasks = CoupledHeap()
    i = 0
    while i < len(jobs) or tasks.n > 0:
        
        if tasks.n == 0 and i < len(jobs):
            p1 = max(p1 , jobs[i][0])
            p2 = max(p2 , jobs[i][0])
            t = min(p1 , p2)
        
        while i < len(jobs) and (jobs[i][0] <= t and jobs[i][0] <= t):
            j = jobs[i]
            tasks.enqueue(-i , j[3]/j[1] , j[4]/j[2])
            i += 1
        
        if t >= p1 and tasks.n > 0:
            x = tasks.extractMaxX()
            total_profit += jobs[-x[0]][3]
            p1 = t + jobs[-x[0]][1]
            total_time += t - jobs[-x[0]][0]
        
        if t >= p2 and tasks.n > 0:
            y = tasks.extractMaxY()
            total_profit += jobs[-y[0]][4]
            p2 = t + jobs[-y[0]][2]
            total_time += t - jobs[-y[0]][0]
        
        t = min(p1 , p2)
        
    return (total_profit , total_time)
            
        
    
    
