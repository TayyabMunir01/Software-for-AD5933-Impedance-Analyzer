def get_reg_1(number):																			# Get Register 1
	if number<=255:
		return 0
		
	if number>255 and number<= 65535:
		return 0

	if number>65535 and number<=16777215:
		i = 0
		while number>65535:
		 	number = number - 65536
		 	i = i+1
		return i

def get_reg_2(number):																			# Get Register 2
	if number<=255:
		return 0
		
	if number>255 and number<= 65535:
		i = 0
		while number>255:
		 	number = number - 256
		 	i = i+1
		return i

	if number>65535 and number<=16777215:
		i = 0
		j = 0
		while number>65535:
		 	number = number - 65536
		 	i = i+1
		while number>255:
		 	number = number - 256
		 	j = j+1
		return j

def get_reg_3(number):																			# Get Register 3
	if number<=255:
		return number

	if number>255 and number<= 65535:
		i = 0
		while number>255:
		 	number = number - 256
		 	i = i+1
		return number
		
	if number>65535 and number<=16777215:
		i = 0
		j = 0
		while number>65535:
		 	number = number - 65536
		 	i = i+1
		while number>255:
		 	number = number - 256
		 	j = j+1
		return number

# print(get_reg_1(16777215))
# print(get_reg_2(65535))
# print(get_reg_3(255))

# number = int(input("enter number to split: "))
# print(get_reg_1(number))
# print(get_reg_2(number))
# print(get_reg_3(number))


# def get_reg_2_inc(number):																			# Get Register 2 for special case number of increments
# 	if number <=511:	
# 		if number<=255:
# 			return 0
			
# 		if number>255 and number<= 65535:
# 			i = 0
# 			while number>255:
# 			 	number = number - 256
# 			 	i = i+1
# 			return i

# 		if number>65535 and number<=16777215:
# 			i = 0
# 			j = 0
# 			while number>65535:
# 			 	number = number - 65536
# 			 	i = i+1
# 			while number>255:
# 			 	number = number - 256
# 			 	j = j+1
# 			return j

# def get_reg_3_inc(number):
# 	if number <= 511:																		# Get Register 3 for special case number of increments
# 		if number<=255:
# 			return number

# 		if number>255 and number<= 65535:
# 			i = 0
# 			while number>255:
# 			 	number = number - 256
# 			 	i = i+1
# 			return number
			
# 		if number>65535 and number<=16777215:
# 			i = 0
# 			j = 0
# 			while number>65535:
# 			 	number = number - 65536
# 			 	i = i+1
# 			while number>255:
# 			 	number = number - 256
# 			 	j = j+1
# 			return number






# def reg_splitter(number):																	Template for splitting into three regiters
# 	if number<=255:
# 		start_freq_req_1 = 0
# 		start_freq_req_2 = 0
# 		start_freq_req_3 = number
# 		print(str(start_freq_req_1) +"   " +str(start_freq_req_2)+"   "+str(start_freq_req_3))

# 	if number>255 and number<= 65535:
# 		start_freq_req_1 = 0
# 		i = 0
# 		while number>255:
# 		 	number = number - 256
# 		 	i = i+1
# 		start_freq_req_2 = i
# 		start_freq_req_3 = number
# 		print(str(start_freq_req_1) +"   " +str(start_freq_req_2)+"   "+str(start_freq_req_3))

# 	if number>65535 and number<=16777215:
# 		i = 0
# 		j = 0
# 		while number>65535:
# 		 	number = number - 65536
# 		 	i = i+1
# 		while number>255:
# 		 	number = number - 256
# 		 	j = j+1
# 		start_freq_req_1 = i
# 		start_freq_req_2 = j
# 		start_freq_req_3 = number
# 		print(str(start_freq_req_1) +"   " +str(start_freq_req_2)+"   "+str(start_freq_req_3))

# 	else:
# 		print("number is less than 255")

# # number=int(input("enter the number:  "))
# # func(number)