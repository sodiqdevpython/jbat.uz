from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from school.models import OverallClasses, Organizations, RoomsType, Rooms, RoomsEquipment, UserProfile
from .forms import OverallClassesForm, RoomsTypeForm, RoomForm, RoomsEquipmentForm
from django.db.models import Count


@login_required
def home(request):
    user_profile = request.user.user_profile
    organizations = Organizations.objects.filter(admin=user_profile)

    if organizations.exists():
        organization_instance = organizations.first()  # Handle the first organization

        # Get RoomsEquipment for the user
        equipment = RoomsEquipment.objects.filter(author=user_profile)[:5]

        # Get Rooms for the organization
        rooms = Rooms.objects.filter(organization=organization_instance)[:5]

        # Get RoomsType statistics for the organization
        rooms_type_stats = RoomsType.objects.filter(organization=organization_instance).annotate(count=Count('id'))[:5]

        # Get OverallClasses for the organization
        overall_classes = OverallClasses.objects.filter(organization=organization_instance).annotate(count=Count('id'))[:5]

        # Prepare data for charts
        room_types = [room_type.name for room_type in rooms_type_stats]
        room_counts = [room_type.count for room_type in rooms_type_stats]

        overall_class_names = [cls.name for cls in overall_classes]
        overall_class_counts = [cls.count for cls in overall_classes]

        context = {
            'equipment': equipment,
            'rooms': rooms,
            'room_types': room_types,
            'room_counts': room_counts,
            'overall_class_names': overall_class_names,
            'overall_class_counts': overall_class_counts,
        }
    else:
        context = {
            'equipment': [],
            'rooms': [],
            'room_types': [],
            'room_counts': [],
            'overall_class_names': [],
            'overall_class_counts': [],
        }

    return render(request, 'employee/home.html', context)

@login_required
def class_list(request):
    get_list = OverallClasses.objects.filter(organization__admin = request.user.user_profile, is_active=True)
    user_org = get_object_or_404(Organizations, admin = request.user.user_profile)
    rooms_types = RoomsType.objects.filter(organization = user_org, is_active=True)
    form = OverallClassesForm()

    context = {
        'data': get_list,
        'rooms_types': rooms_types,
        'form': form
    }
    return render(request, 'employee/class-list.html', context)

@login_required
def create_overall_class(request):
    get_user = get_object_or_404(Organizations, admin=request.user.user_profile)

    if request.method == 'POST':
        form = OverallClassesForm(request.POST or None)
        if form.is_valid():
            new_overall_class = form.save(commit=False)
            new_overall_class.organization = get_user
            new_overall_class.save()
            return redirect('class_list')


@login_required
def delete_overall_class(request, id):
    get_data = get_object_or_404(OverallClasses, id=id)
    get_data.is_active = False
    get_data.save()
    return redirect('class_list')


@login_required
def create_room_type(request):
    if request.method == 'POST':
        form = RoomsTypeForm(request.POST or None)
        get_user = get_object_or_404(Organizations, admin = request.user.user_profile)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.organization = get_user
            new_room.save()
            return redirect('class_list')
        
@login_required
def delete_rooms_type(request, id):
    get_data = get_object_or_404(RoomsType, id=id)
    get_data.is_active = False
    get_data.save()
    return redirect('class_list')


@login_required
def create_room(request):
    author = request.user.user_profile
    org = get_object_or_404(Organizations, admin=author)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.organization = org
            new_room.author = author
            new_room.save()
            return redirect('rooms_list')
        
@login_required
def delete_room(request, id):
    get_data = get_object_or_404(Rooms, id=id)
    get_data.is_active = False
    get_data.save()
    return redirect('rooms_list')


@login_required
def room_list(request):

    get_org = get_object_or_404(Organizations, admin=request.user.user_profile)

    get_rooms = Rooms.objects.filter(organization=get_org, is_active=True)

    context = {
        'overall_classes': OverallClasses.objects.filter(organization=get_org, is_active=True),
        'room_categories': RoomsType.objects.filter(organization=get_org, is_active=True),
        'rooms': get_rooms
    }

    return render(request, 'employee/rooms-list.html', context)

@login_required
def update_room(request, id):
    room = get_object_or_404(Rooms, id=id)
    get_org = get_object_or_404(Organizations, admin=request.user.user_profile)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms_list')
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
        'room': room,
        'overall_classes': OverallClasses.objects.filter(organization=get_org, is_active=True),
        'room_categories': RoomsType.objects.filter(organization=get_org, is_active=True),
    }
    return render(request, 'employee/update-room.html', context)


@login_required
def equipment_list(request):
    get_org = get_object_or_404(Organizations, admin=request.user.user_profile)
    equipment_list = RoomsEquipment.objects.filter(is_active=True, room__organization=get_org).order_by('-accepted_date')
    context = {
        'equipment_list': equipment_list,
    }
    return render(request, 'employee/equipment-list.html', context)

@login_required
def create_equipment(request):

    # get_org = get_object_or_404(Organizations, admin=request.user.user_profile)
    get_rooms = Rooms.objects.filter(author=request.user.user_profile)

    if request.method == 'POST':
        form = RoomsEquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_equipment = form.save(commit=False)
            new_equipment.author = request.user.user_profile
            new_equipment.save()
            return redirect('equipment_list')
    else:
        form = RoomsEquipmentForm()
    return render(request, 'employee/create-equipment.html', {'form': form, 'rooms': get_rooms})


# @login_required
# def update_equipment(request, id):
#     get_data = get_object_or_404(RoomsEquipment, id=id)

#     if request.method == 'POST' and (request.user.is_superuser or get_data.admin == request.user.user_profile):
#         form = RoomsEquipmentForm(request.POST or None, request.FILES or None, instance=get_data)
#         if form.is_valid():
#             form.save()
#             return redirect('equipment_list')
#     else:
#         form = RoomsEquipmentForm(instance=get_data)
    
#     context = {
#         'form': form,
#         'dt': get_data
#     }

#     return render(request, 'employee/update-equipment.html', context)

class EquipmentUpdateView(UpdateView):
    model = RoomsEquipment
    form_class = RoomsEquipmentForm
    template_name = 'employee/update-equipment.html'
    context_object_name = 'equipment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = RoomsEquipment.objects.all()  # Xonalar ro'yxati
        context['selected_room_id'] = self.object.room.id if self.object.room else None  # Tanlangan xonani olish
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

@login_required
def delete_equipment(request, id):
    get_equipment = get_object_or_404(RoomsEquipment, id=id)
    if get_equipment.author == request.user.user_profile:
        get_equipment.is_active = False
        get_equipment.save()
        return redirect('equipment_list')


@login_required
def equipment_detail(request, pk):
    
    get_data = get_object_or_404(RoomsEquipment, pk=pk)

    context = {
        'equipment': get_data
    }

    return render(request, 'employee/equipment_detail.html', context)