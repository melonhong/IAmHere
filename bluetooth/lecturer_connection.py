import subprocess
import time
import pexpect
import sys

# 1. 페어링 메서드
def pair_device(mac_address):
    try:
        # bluetoothctl 명령을 실행하고 대화식으로 처리
        child = pexpect.spawn('bluetoothctl', encoding='utf-8', logfile=sys.stdout)

        # 블루투스 프롬프트가 뜰 때까지 대기
        child.expect('Agent registered')
        child.sendline('scan on')
        time.sleep(10)
        child.sendline('scan off')
        child.sendline(f'pair {mac_address}')

        # 'yes' 입력을 기다린 후 자동으로 'yes' 입력
        idx = child.expect(r'Confirm passkey \d+ \(yes/no\):')

        if idx == 0:
            child.sendline('yes')
            time.sleep(5)
            child.sendline(f'trust {mac_address}')
        elif idx == 1:
            # 바로 페어링 완료된 경우
            pass
        else:
            print("❌ 페어링 중 오류가 발생했습니다.")
            child.sendline('exit')
            return

        # 페어링 완료 후 bluetoothctl 종료
        child.sendline('exit')
        child.close()

        print("✅ 페어링이 완료되었습니다.")
        
    except pexpect.ExceptionPexpect as e:
        print(f"❌ 예외 발생: {e}")

# 2. 연결 메서드
def connect_device(mac_address):
    try:
        # 연결 시도
        result = subprocess.run(["bluetoothctl", "connect", mac_address], capture_output=True, text=True)
        if "Connection successful" in result.stdout:
            print(f"✅ {mac_address} 연결 성공")
            return True
        else:
            print(f"❌ {mac_address} 연결 실패")
            print(result.stdout)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 연결 중 오류 발생: {e}")
        return False

# 3. 연결 감시 메서드
def is_connected(mac_address):
    try:
        # 연결 상태 확인
        result = subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True)
        if "Connected: yes" in result.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 연결 상태 감시 중 오류 발생: {e}")

def monitor_connection(mac_address):
    print(f"🔍 '{mac_address}' 연결 상태 모니터링 시작...")
    try:
        while True:
            if not is_connected(mac_address):
                print("⚠️ 디바이스 연결이 끊어졌습니다!")
                break
            time.sleep(1)  # 1초마다 체크
    except KeyboardInterrupt:
        print("\n🛑 모니터링을 수동으로 종료했습니다.")
