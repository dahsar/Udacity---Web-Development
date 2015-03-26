import string

def newin(index):
	if index + 13 > 25:
		diff = 26 - index - 1
		return 13 - diff - 1
	else:
		return index + 13

def rot13(text):
	i = 0
	while i < len(text):
		if text[i] in string.ascii_lowercase:
			for x in range(0, 26):
				if text[i] == string.ascii_lowercase[x]:
					index = x
					break
			index = newin(index)
			#text[i] = string.ascii_lowercase[index] //illegal
			text = text[:i] + string.ascii_lowercase[index] + text[i+1:]
			
		if text[i] in string.ascii_uppercase:
			for x in range(0,26):
				if text[i] == string.ascii_uppercase[x]:
					index = x
					break
			index = newin(index)
			#text[i] = string.ascii_uppercase[index]
			text = text[:i] + string.ascii_uppercase[index] + text[i+1:] 
		i = i + 1	
	return text	
