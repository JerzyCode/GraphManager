shift + left m button - add vertex
alt + left m button - check vertex to add edge


PLAN:
 - zapobiec sytuacji, w której użytkownik otworzy okno dodawania grafu oraz generowania na raz,
    bo jak kliknie generuj, to moze wtedy zmienic parametry dodawania i sie psuje
 - przy zaznaczaniu digraph, ma sie zaznaczać też directed
 - naprawić algorytmy, ten sleep nie działa poprawnie, chce zeby sie wykonywał na oddzielnym wątku
    żeby można było klikac w aplikacji