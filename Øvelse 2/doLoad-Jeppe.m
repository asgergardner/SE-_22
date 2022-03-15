function [data error] = doLoad(filepath)

%% Initialize data Header
% In case no values are found in data file, just keep 0. 

Header = struct();
name_flag = 0;

%% read file line by line to get header

f = fopen(filepath,'r');
nline = @(f) sprintf('%s\n',strtrim(fgets(f))); %printing next line of f
tline = nline(f);
s = '';


while (~strcmp(strtrim(tline),'[AndorNewton]')) && ischar(tline)
    s = [s,tline];
    tline = nline(f); % Reads the next line of file
end

% Write stuff to header file

Header.full = s;


%% Read data from file
datablock = '%s%s%s%s';
rawdata = textscan(f,datablock,'delimiter',{'\t'}); % reading data -> 2-dimensional cell array of strings
fclose(f);                                          % {1} = name
                                                    % {2} = value (string)



%% Generating a list of fields contained in the datafile
input_names = {'wavelength','Bg','Sig','Ref'};

for k = 1:4
    temp = rawdata{k};
    if k == 1
        data_cell{k} = cell2mat(cellfun(@str2num,(temp(1:end-2)),'UniformOutput',0));
    else
        data_cell{k} = cell2mat(cellfun(@str2num,(temp(1:end-1)),'UniformOutput',0));
    end
end

input_names = matlab.lang.makeValidName(input_names,'replacementstyle','delete');
% Generates valid matlab names for each parameter name. Changing eg. '.' to
% '_' and so on.


%% making the final data structure
data = cell2struct(data_cell,input_names,2); % putting the data into the matching fieldnames

% adding some extracted data from the header
data.Header = Header;