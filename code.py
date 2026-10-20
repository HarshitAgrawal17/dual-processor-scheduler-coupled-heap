"""
Coupled Heap for 2-Processor Scheduling.

"""
def element ( id, x_pri, y_pri, x_ind = None, y_ind = None):
    return {'id':id , 'x_pri': x_pri, 'y_pri': y_pri, 'x_ind': x_ind, 'y_ind': y_ind}
        
class CoupledHeap:
    """
    A heap over two independent priority axes, X and Y.

    Elements are (id, x_pri, y_pri). Priorities are numbers (ints or floats); larger
    means higher priority. On a tie, the larger id wins, on both axes.
    """

    def __init__(self):
        self.heapx = []
        self.heapy = []
        self.n = 0
        pass

    # -------- Do not change the following functions' names, signatures --------

    def enqueue(self, id, x_pri, y_pri):
        if self.n == 0:
            e = element(id, x_pri, y_pri, 0 , 0)
            self.heapx.append(e)
            self.heapy.append(e)
            
        else:
            e = element(id, x_pri, y_pri, self.n , self.n)
            self.heapx.append(e)
            self.heapy.append(e)
            self.heap_up_x(self.n)
            self.heap_up_y(self.n)
        
        self.n += 1    
        """Insert an element. O(log n) worst case."""
        
        pass
    
    def swapx(self, e1, e2):
        x1,x2 = e1['x_ind'],e2['x_ind']
        self.heapx[x1], self.heapx[x2] = self.heapx[x2], self.heapx[x1]
        self.heapx[x1]['x_ind'], self.heapx[x2]['x_ind'] = x1, x2
        self.heapy[e1['y_ind']]['x_ind'] = x2
        self.heapy[e2['y_ind']]['x_ind'] = x1
        
    def swapy(self, e1, e2):
        y1,y2 = e1['y_ind'],e2['y_ind']
        self.heapy[y1], self.heapy[y2] = self.heapy[y2], self.heapy[y1]
        self.heapy[y1]['y_ind'], self.heapy[y2]['y_ind'] = y1, y2
        self.heapx[e1['x_ind']]['y_ind'] = y2
        self.heapx[e2['x_ind']]['y_ind'] = y1
        
    def heap_up_x(self, ix):
        current_index = ix
        parent_index = (current_index-1)//2
        current_element = self.heapx[ix]
        parent_element = self.heapx[parent_index]
        while True:
            if current_index == 0: return
        
            if current_element['x_pri'] < parent_element['x_pri']: return
        
            elif current_element['x_pri'] == parent_element['x_pri']:
                if current_element['id'] < parent_element['id']: return
                else: self.swapx(current_element, parent_element)
                
            else: self.swapx(current_element, parent_element)
            
            current_index = parent_index
            parent_index = (current_index - 1) // 2
            parent_element = self.heapx[parent_index]
            current_element = self.heapx[current_index]
    def heap_up_y(self, iy):
        current_index = iy
        parent_index = (current_index-1)//2
        current_element = self.heapy[iy]
        parent_element = self.heapy[parent_index]
        while True:
            if current_index == 0: return
        
            if current_element['y_pri'] < parent_element['y_pri']: return
        
            elif current_element['y_pri'] == parent_element['y_pri']:
                if current_element['id'] < parent_element['id']: return
                else: self.swapy(current_element, parent_element)
                
            else: self.swapy(current_element, parent_element)
            
            current_index = parent_index
            parent_index = (current_index - 1) // 2
            parent_element = self.heapy[parent_index]
            current_element = self.heapy[current_index]
        
    def peekMaxX(self):
        """Max X-priority element as (id, x_pri, y_pri); None if empty. O(1)."""
        if self.n == 0: return None
        e = self.heapx[0]
        return (e['id'] , e['x_pri'] , e['y_pri'])

    def peekMaxY(self):
        """Max Y-priority element as (id, x_pri, y_pri); None if empty. O(1)."""
        if self.n == 0: return None
        e = self.heapy[0]
        return (e['id'] , e['x_pri'] , e['y_pri'])

    def find_child_ind_x(self, curr_ind):
        curr_ind = curr_ind
        child_index_1 = 2 * curr_ind + 1
        child_index_2 = 2 * curr_ind + 2
        if child_index_1 >= self.n : return None
        
        c1 = self.heapx[child_index_1]
        if child_index_2 < self.n:
            c2 = self.heapx[child_index_2] 
            v1 = c1['x_pri']
            v2 = c2['x_pri']
            if v1 == v2:
                p1 = c1['id']
                p2 = c2['id']
                if p1 > p2:
                    ind = child_index_1
                else: ind = child_index_2
            elif v1 > v2 : ind = child_index_1
            else : ind = child_index_2
            
        else: ind = child_index_1
        return ind
        
    def find_child_ind_y(self, curr_ind):
        curr_ind = curr_ind
        child_index_1 = 2 * curr_ind + 1
        child_index_2 = 2 * curr_ind + 2
        if child_index_1 >= self.n : return None
        
        c1 = self.heapy[child_index_1]
        if child_index_2 < self.n:
            c2 = self.heapy[child_index_2] 
            v1 = c1['y_pri']
            v2 = c2['y_pri']
            if v1 == v2:
                p1 = c1['id']
                p2 = c2['id']
                if p1 > p2:
                    ind = child_index_1
                else: ind = child_index_2
            elif v1 > v2 : ind = child_index_1
            else : ind = child_index_2
            
        else: ind = child_index_1
        return ind
    def heap_down_x(self, curr_ind):
        child_ind = self.find_child_ind_x(curr_ind)
        
        if not child_ind : return 
    
        # finally curr_ind, child_ind (child index to be swapped with, if swapped)
        while True:
            if curr_ind >= self.n or not child_ind: return
        
            if self.heapx[curr_ind]['x_pri'] > self.heapx[child_ind]['x_pri']: return
        
            elif self.heapx[curr_ind]['x_pri'] == self.heapx[child_ind]['x_pri']:
                if self.heapx[curr_ind]['id'] > self.heapx[child_ind]['id']: return
                else: self.swapx(self.heapx[curr_ind], self.heapx[child_ind])
                
            else: self.swapx(self.heapx[curr_ind], self.heapx[child_ind])
            
            curr_ind = child_ind
            child_ind = self.find_child_ind_x(child_ind)

    def extractMaxX(self):
        if self.n == 0: return None
       
        if self.n == 1 :  
            x_removed = self.heapx.pop()
            self.heapy.pop()
            self.n -= 1
        else:    
            # Remove element from x
            x_removed = self.heapx[0] 
            # pop last and put there
            self.heapx[0] = self.heapx.pop()

            #remove the corresponding element from y
            y_remove_index = x_removed['y_ind']
            if y_remove_index == self.n - 1 : 
                self.heapy.pop()
                self.n -= 1

                #Match the x indices
                self.heapx[0]['x_ind'] = 0
                self.heapy[self.heapx[0]['y_ind']]['x_ind'] = 0
                self.heap_down_x(0)
            else:
                # pop last element and put there
                self.heapy[y_remove_index] = self.heapy.pop()

                self.n -= 1

                #Match the y indices
                self.heapy[y_remove_index]['y_ind'] = y_remove_index
                p = self.heapy[y_remove_index]['x_ind']
                if p == self.n : p = 0 #Since it is the popped element
                self.heapx[p]['y_ind'] = y_remove_index 

                #Match the x indices
                self.heapx[0]['x_ind'] = 0
                self.heapy[self.heapx[0]['y_ind']]['x_ind'] = 0

                self.heap_down_x(0)
                self.heap_up_y(y_remove_index)
                self.heap_down_y(y_remove_index)
                

        e = x_removed
        return (e['id'] , e['x_pri'] , e['y_pri'])
    def heap_down_y(self, curr_ind):
        child_ind = self.find_child_ind_y(curr_ind)
        
        if not child_ind : return 
    
        # finally curr_ind, child_ind (child index to be swapped with, if swapped)
        while True:
            if curr_ind >= self.n or not child_ind: return
        
            if self.heapy[curr_ind]['y_pri'] > self.heapy[child_ind]['y_pri']: return
        
            elif self.heapy[curr_ind]['y_pri'] == self.heapy[child_ind]['y_pri']:
                if self.heapy[curr_ind]['id'] > self.heapy[child_ind]['id']: return
                else: self.swapy(self.heapy[curr_ind], self.heapy[child_ind])
                
            else: self.swapy(self.heapy[curr_ind], self.heapy[child_ind])
            
            curr_ind = child_ind
            child_ind = self.find_child_ind_y(child_ind)

    def extractMaxY(self):
        if self.n == 0: return None
       
        if self.n == 1 :  
            y_removed = self.heapy.pop()
            self.heapx.pop()
            self.n -= 1
        else:    
            # Remove element from y
            y_removed = self.heapy[0] 
            # pop last and put there
            self.heapy[0] = self.heapy.pop()

            #remove the corresponding element from y
            x_remove_index = y_removed['x_ind']   
            if x_remove_index == self.n - 1 : 
                self.heapx.pop()
                self.n -= 1
    
                #Match the y indices
                self.heapy[0]['y_ind'] = 0
                self.heapx[self.heapy[0]['x_ind']]['y_ind'] = 0
                self.heap_down_y(0)
            else:
                # pop last element and put there
                self.heapx[x_remove_index] = self.heapx.pop()
    
                self.n -= 1
    
                #Match the x indices
                self.heapx[x_remove_index]['x_ind'] = x_remove_index
                p = self.heapx[x_remove_index]['y_ind']
                if p == self.n: p = 0 #Since its the popped element
                self.heapy[p]['x_ind'] = x_remove_index
    
                #Match the y indices
                self.heapy[0]['y_ind'] = 0
                self.heapx[self.heapy[0]['x_ind']]['y_ind'] = 0
    
                self.heap_down_y(0)
                self.heap_up_x(x_remove_index)
                self.heap_down_x(x_remove_index)
        e = y_removed
        return (e['id'] , e['x_pri'] , e['y_pri'])

def solve_scheduling(jobs):
    """
    Simulate the two processors and return (total_profit, total_waiting_time).

    jobs: list of (t_i, t0_i, t1_i, p0_i, p1_i), sorted by arrival time t_i.

    Target: O(N log N) time, O(N) space.
    """
    # We will put negative of id in the coupled heap
    waiting_time = 0
    total_profit = 0
    idle1 = 0
    idle2 = 0
    updation_time = 0
    i = 0
    num = len(jobs)
    heap = CoupledHeap()
    while True :
        if i == num and heap.n == 0:
            break
        if heap.n == 0:
            next_arrival = jobs[i][0]
            if idle1 <= next_arrival and idle2 <= next_arrival:
                updation_time = next_arrival
                idle1 = idle2 = next_arrival
            else:
                updation_time = min(max(idle1 , idle2) , next_arrival)
        
        while i < num and jobs[i][0] <= updation_time:
            job = jobs[i]
            heap.enqueue(-i, job[3]/job[1] , job[4]/job[2])
            i += 1
        
        if idle1 <= updation_time:
            x = heap.extractMaxX()
            if x:
                start_time = max(idle1, updation_time)
                waiting_time += start_time - jobs[-x[0]][0]
                idle1 = updation_time + jobs[-x[0]][1]
                total_profit += jobs[-x[0]][3]
                
        if idle2 <= updation_time:
            y = heap.extractMaxY()
            if y:
                start_time = max(idle2, updation_time)
                waiting_time += start_time - jobs[-y[0]][0]
                idle2 = updation_time + jobs[-y[0]][2]
                total_profit += jobs[-y[0]][4]
                
        
        times = []
        if idle1 > updation_time:
            times.append(idle1)
        if idle2 > updation_time:
            times.append(idle2)
        if i < num :
            p = jobs[i][0]
            if p > updation_time:
                times.append(p)
            
            
        if times : updation_time = min(times)
        else : break
        
        
        
        
        
        
            
        
    return (total_profit , waiting_time)      
