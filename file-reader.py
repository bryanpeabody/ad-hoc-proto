import struct
import locale

total_debits = 0
total_credits = 0
total_auto_pays_started = 0
total_auto_pays_ended = 0
search_user_id = 2456938384156277127
search_user_id_balance = 0

# Setup the locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#
# 1. Open and read in a binary file.
# 2. Pull out the header row, all values are in big endian. Store the number of records to expect.
# 3. Loop over each record after the header. Keep track of totals.
# 4. When we have processed all records, exit the loop and print results.
#
with open("txnlog.dat", "rb") as bfile:

	try:
		#
		# Start at the begining of the file
		#
		bfile.seek(0)
	
		#
		# Lets start with reading the header. For this homework, we'll keep it simple and assume
		# the header is always there.
		#
        	# The header looks like this:
		# | 4 byte magic string "MPS7" | 1 byte version | 4 byte (uint32) # of records |
		#
		magic_string = int.from_bytes(bfile.read(4), byteorder='big')
		version = struct.unpack('>b', bfile.read(1))[0]
		total_records = struct.unpack('>i', bfile.read(4))[0]

		#
		# Loop over the records until we process "total_records"
		#
		count = 0
		while count <= total_records:
			#
			# Try to read each record. They look like this:
			# 1 byte record type enum | 4 byte (uint32) Unix timestamp | 8 byte (uint64) user ID 
			#

			#
			# Get the enum type
			#
			enum_type_chunk = bfile.read(1)
			enum_type = struct.unpack('>b', enum_type_chunk)[0]
		
			#
			# Get the timestamp. Not used for anything.
			#	
			time_stamp_chunk = bfile.read(4)
	
			#
			# Get the user id. Used to searching for a specific user.
			#	
			user_id_chunk = bfile.read(8)
			user_id = struct.unpack('>Q', user_id_chunk)[0]
			
			#
			# Initial the amount to 0.
			#
			amount = 0
		
			# If this is a credit or debit also get the amount.
			if enum_type == 0 or enum_type == 1:
				amount_chunk = bfile.read(8)
				amount = struct.unpack('>d', amount_chunk)[0]
		
			# If this is a debit, add the amount.
			if enum_type == 0:
				total_debits += amount
			
			# If this is a credit, add the amount.
			elif enum_type == 1:
				total_credits += amount
		
			# If this is a start auto pay, increment.
			elif enum_type == 2:
				total_auto_pays_started += 1
	
			# If this is an end auto pay, increment.
			elif enum_type == 3:
				total_auto_pays_ended += 1

			# If this is the user we are looking for, update the balance. 
			if user_id == search_user_id:
				# Debit
				if enum_type == 0:
					search_user_id_balance -= amount

				# Credit
				if enum_type == 1:
					search_user_id_balance += amount
			
			# Increment loop varible
			count += 1
	except:
		print("General exception.")
	
	finally:
		#
		# Close the file
		#
		bfile.close()		
	
		#	
		# Print the results
		#
		print("Total amount of debits: $%s" % locale.format("%.2f", total_debits, True, True))
		print("Total amount of credits: $%s" % locale.format("%.2f", total_credits, True, True))
		print("Total number of autopays started: %i" % total_auto_pays_started)
		print("Total number of autopays ended: %i" %total_auto_pays_ended)
		print("Balance for user %i is: $%s" % (search_user_id, locale.format("%.2f", search_user_id_balance, True, True)))

