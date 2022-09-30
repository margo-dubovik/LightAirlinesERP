import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_staff_profile_redirect(client, testsupervisorprofile, testgatemanagerprofile, testcheckinmanagerprofile):
    client.force_login(testsupervisorprofile.user)
    url = reverse('staff-profile-redirect')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse('supervisor-profile', kwargs={'id': testsupervisorprofile.pk})

    client.get(reverse('logout'))

    client.force_login(testgatemanagerprofile.user)
    url = reverse('staff-profile-redirect')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse('gate-manager-profile', kwargs={'id': testgatemanagerprofile.pk})

    client.get(reverse('logout'))

    client.force_login(testcheckinmanagerprofile.user)
    url = reverse('staff-profile-redirect')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == reverse('checkin-manager-profile', kwargs={'id': testcheckinmanagerprofile.pk})

    client.get(reverse('logout'))



