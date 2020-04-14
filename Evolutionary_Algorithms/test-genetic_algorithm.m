addpath(genpath('.\2005'))

functions = [1 2 3 4 5 6 7 8 9 10]; % Functions being solved
%functions = [3 6 9];
numF = size(functions, 2);
nTimes = 20;            % Number of times in which a function is going to be solved
dimension = 30;         % Dimension of the problem

% GA parameters
populationSize = 100;
elitismSize = 10;
TS_k = 2;               % Tournament selection size
pCrossover = 0.8;       % Probability of crossover
pMutation = 0.3;        % Probability of mutation
alfa = 0.1;             % For blended crossover - "The higher the value of alpha the more explorative the search"
sigma = 2.0;            % For mutation

for i = 1:numF
    
    fitfun = functions(i); % fitfun is the function that we are solving
    fprintf('\n-----  Function %d started  -----\n\n', fitfun);
    
    for t = 1:nTimes
        
        maxEval = 10000 * dimension; % Maximum number of evaluation
        [value, upper, lower, objetiveValue, o, A, M, a, alpha, b] = getInformation_2005(fitfun, dimension);
        currentEval = 0;

        % Start generating the initial population
        population = zeros(populationSize, dimension);
        for j = 1:populationSize
            population(j,:) = lower + (upper - lower).*rand(1, dimension);
        end

        populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); % Fitness values of all individuals (smaller value is better)
        bestSolutionFitness = min(populationFitness);
        currentEval = currentEval + populationSize;
        
        fprintf('>> %dth run, Initial best individual fitness: %d\n', t, bestSolutionFitness); % Temp

        % Algorithm loop
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
            % Sort population by fitness
            [populationFitnessSorted, sortedFitnessIndex] = sort(populationFitness);
            populationSorted = population(sortedFitnessIndex,:);
            
            offspring = zeros(populationSize, dimension);
            c = zeros(2, dimension);
            for j = 1:2:populationSize - elitismSize + 1
                %* Choose parents using tournament selection
                for k = 1:2
                    kInds = randperm(populationSize, TS_k);
                    for l = 1:populationSize
                        if any(kInds(:) == sortedFitnessIndex(l))
                            c(k,:) = populationSorted(l,:);
                            break
                        end
                    end
                end

%                 % old
%                 k = 1;
%                 while k <= 2
%                     kInds = randperm(populationSize, TS_k); % select k individuals at random
%                     for l = 1:populationSize
%                         ki = find(kInds == sortedFitnessIndex(l)); %, 1, 'first');
%                         if (ki > 0) & (pCrossover * ((1 - pCrossover)^(ki - 1)) > rand())
%                                 c(k,:) = populationSorted(l,:);
%                                 k = k + 1;
%                                 break
%                         end
%                     end
%                 end
                
                % Recombine parents to generate a set of offspring
                cMin = min(c(1,:), c(2,:));
                cMax = max(c(1,:), c(2,:));
                I = cMax - cMin;
                lo = (cMin - I * alfa);
                hi = (cMax + I * alfa);
                offspring(j,:)     = lo + (hi - lo).*rand(1, dimension);
                offspring(j + 1,:) = lo + (hi - lo).*rand(1, dimension);

%                 % old
%                 if pCrossover > rand(); offspring(j,:)   = lo + (hi - lo).*rand(1, dimension);
%                 else;                   offspring(j,:)   = c(1,:); end
%                 if pCrossover > rand(); offspring(j+1,:) = lo + (hi - lo).*rand(1, dimension);
%                 else;                   offspring(j+1,:) = c(2,:); end
                
            end

            % Mutate offspring
            for j = 1:populationSize
                if pMutation > rand()
                    u = sqrt(sigma) * randn(1, dimension);
                    offspring(j,:) = offspring(j,:) + u;
                end
            end

            % Replace population by the set of new offspring
            offspring(end - elitismSize + 1:end, :) = populationSorted(1:elitismSize, :);
            population = offspring;
  
            % Evaluate fitness of each individual
            populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b);
            bestSolutionFitness = min(populationFitness);
            currentEval = currentEval + populationSize;
        
        end

        % Best individual
        bestSolutionFitness = min(populationFitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
                
    end
    
end
