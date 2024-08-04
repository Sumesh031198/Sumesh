select *
from CovidDeaths$
order by 3,4

--select *
--from CovidVaccinations$
--order by 3,4

--select data for analysis

select location,date,total_cases,new_cases,total_deaths,population
from CovidDeaths$
order by 1,2

--total cases versus total deaths as death percentage per country
select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as death_percentage
from CovidDeaths$
where location like '%states%'
order by 1,2

--total cases versus population
select location, date, total_cases, population, (total_cases/population)*100 as affectedrate
from CovidDeaths$
order by 1,2 

--country with highest infection rate--
select location,MAX(total_cases) as highestcovidcount, population, (MAX(total_cases)/population)*100 as affectedrate
from CovidDeaths$
group by Location, population
order by affectedrate desc

--countries with highest deathcount--
select location,MAX(cast(total_deaths as int)) as highestdeathcount, population, (MAX(total_deaths)/population)*100 as deathrate
from CovidDeaths$
group by Location, population
order by deathrate desc

--covdi count by continent
select location, MAX(cast(total_deaths as int)) as highestdeathcount
from CovidDeaths$
where continent is null 
group by location
order by highestdeathcount desc


--death count by continent
select continent, MAX(cast(total_deaths as int)) as highestdeathcount
from CovidDeaths$
where continent is not null 
group by continent
order by highestdeathcount desc

--global covid count
select  sum(new_Cases) as total_Cases,sum(cast(new_deaths as int)) as total_deaths, sum(cast(new_deaths as int))/sum(new_Cases)*100 as death_percentage--  total_cases, total_deaths, (total_deaths/total_cases)*100 as death_percentage
from CovidDeaths$
where continent is not null
--group by date
order by 1,2


Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date)  as Rollingpeoplevaccinated
from CovidDeaths$ dea 
join CovidVaccinations$ vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

-- use cte--

with popvsVac (Continent, Location, Date, Population, New_vaccinations, Rollingpeoplevaccinated)
as 
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date)  as Rollingpeoplevaccinated
--,(Rollingpeoplevaccinated/population)*100
from CovidDeaths$ dea 
join CovidVaccinations$ vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
)
select*,(Rollingpeoplevaccinated/Population)*100
from popvsVac

--temp table
DROP table if exists #percentPopulationVaccinated
Create TABLE #percentPopulationVaccinated
(
continent nvarchar(255),
Location nvarchar(255),
Date datetime,
POpulation numeric,
New_vaccinations numeric,
Rollingpeoplevaccinated numeric
)
Insert into #percentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date)  as Rollingpeoplevaccinated
from CovidDeaths$ dea 
join CovidVaccinations$ vac
	on dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

select*,(Rollingpeoplevaccinated/Population)*100
from #percentPopulationVaccinated


--creating views for visualization--

create view percentPopulationVaccinated as 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location,dea.date)  as Rollingpeoplevaccinated
from CovidDeaths$ dea 
join CovidVaccinations$ vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

