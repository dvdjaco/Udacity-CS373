#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       hw3-1.py
#       
#       Copyright 2012 David Jacovkis <david@solaris>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import random

def rand_particles(n_particles, n_states):
  '''return an array "states" with the number of particles in each state
  states[i]'''
  particles = []
  count_states =[0 for n in range(n_states)]
  
  for i in range(n_particles):
    count_states[random.choice(range(n_states))] += 1
  return count_states
  
  
      

def main():
	
  # number of particles and states
  N = 10
  n_states = 4
  cycles = 10000
  
  avg_states = [0 for n in range(n_states)]
  count_zero = 0
  
  for run in range(cycles):
    rand_states = rand_particles(N, n_states)
    avg_states = [avg_states[i] + rand_states[i]  for i in range(n_states)]
    if rand_states[0] == 0: count_zero += 1
  
  avg_states = [float(n)/cycles  for n in avg_states]
  print avg_states, float(count_zero)/cycles
  
  return 0

if __name__ == '__main__':
	main()

