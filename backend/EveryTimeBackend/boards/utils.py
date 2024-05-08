from .models import *
from users.models import User, UserProfile

def CheckBoardPermission(user: User, board: BaseBoard):
    """
        유저의 관련 게시판 열람 권한 확인
        열람 가능 시 True 리턴, 불가 시 False 리턴
    """
    # 전체 공개
    if board.is_public:
        return True
    
    # organizaiton=None인 경우, 전체 관리자
    if user.organization is None:
        return True

    # 전체 공개x
    # 지역 게시판
    if isinstance(board, RegionBoard):
        if user.organization.region == RegionBoard.region: # 해당 지역 소속
            return True
        return False # 해당 지역 비소속 시 열람 불가
        
    # 학교/단체 게시판
    if isinstance(board, OrganizationBoard):
        if user.organization == board.organization: # 해당 학교/단체 소속
            return True
        elif board.is_public_to_region \
        and user.organization.region == OrganizationBoard.region: # 지역 공개 및 해당 지역 소속
            return True
        return False # 해당 학교/단체 비소속 또는 지역 공개이나 해당 지역 비소속
    
    if isinstance(board, ClubBoard):
        user_profile = UserProfile.objects.get(user=user)
        for club in user_profile.clubs:
            if club == ClubBoard.club: # 해당 동아리 소속
                return True
        if board.is_public_to_region \
        and user.organization.region == ClubBoard.region: # 지역 공개 및 해당 지역 소속
            return True
        return False # 해당 학교/단체 비소속 또는 지역 공개이나 해당 지역 비소속
    
    # 에러
    raise Exception('게시판 권한 검사 중 알 수 없는 에러!')